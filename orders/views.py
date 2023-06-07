from typing import Any
from django import http
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from home.models import Product
from .models import Order, OrderItem, Coupon
from orders.forms import CartAddForm, CouponForm
from orders.cart import Cart
import datetime
import requests
import json


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        context = {'cart': cart}
        return render(request, 'orders/cart.html', context)
    
# class AddToCartView(PermissionRequiredMixin, View):
#     permission_required = 'orders.add_rdre'
    
    # def dispatch(self, request, *args, **kwargs):           # if add product need to permission
    #     if not request.user.has_perm('orders.add_rdre'):
    #         raise PermissionDenied()
    #     return super().dispatch(request, *args, **kwargs)

class AddToCartView(View):    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.cart_add(product, form.cleaned_data['quantity'])
        return redirect('home:home')
    
class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove_cart(product)
        return redirect('orders:cart')

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        order = Order.objects.create(user=request.user)
        cart = Cart(request)
        for value in cart:
            OrderItem.objects.create(order=order, product=value['product'], price=value['price'], 
                                     quantity=value['quantity'])
        cart.clear()
        return redirect('orders:order_details', order.id)           

class OrderDetailsView(LoginRequiredMixin, View):
    form_class = CouponForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        context = {'order': order, 'form': self.form_class}
        return render(request, 'orders/order.html', context)

class ApplyCouponView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, order_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data['coupon_code']
            now = datetime.datetime.now()
            try:
                coupon = Coupon.objects.get(code__exact=coupon_code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'The code not exist or expired', 'danger')
                return redirect('orders:order_details', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            
        return redirect('orders:order_details', order_id)        


# sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        request.session['order_pay'] = {
            'order_id': order_id
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)

        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)


            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    zarin_pal_pay = {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    request.session['zarin_pal_pay']=zarin_pal_pay
                    return zarin_pal_pay
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
    
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}
        
class VerifyOrderView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=order_id)
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_total_price(),
        "Authority": request.session['zarin_pal_pay']['authority'],
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

