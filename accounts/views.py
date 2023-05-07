from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import UserLoginForm, UserRegisterForm, VerifyCodeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from utils import send_otp_code
from accounts.models import OTPcode, User
from django.utils.timezone import localtime
import random, datetime

def create_otp(request, phone):
    randome_code = random.randint(1000, 9999)
    OTPcode.objects.create(phone_number=phone, code=randome_code)
    send_otp_code(phone, randome_code)
    messages.success(request, 'Code send for you.', 'success')


class UserRegisterationView(View):
    class_form = UserRegisterForm
    template_name = 'accounts/user_register.html'
    datetime.datetime
    def get(self, request):
        form = self.class_form
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_registeration_info'] = {
                'phone_number':cd['phone_number'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }
            create_otp(request, cd['phone_number'])
            return redirect('accounts:register_verify_code')
        else:
            return render(request, self.template_name,{'form':form})

class UserRegisterationVirifyCodeView(View):
    def get(self, request):
        form = VerifyCodeForm
        return render(request, 'accounts/register_verify_code.html', {'form':form})

    def post(self, request):
        sessions = request.session['user_registeration_info']
        form = VerifyCodeForm(request.POST)
        code_instance = OTPcode.objects.filter(phone_number=sessions['phone_number']).order_by('-created')[0]
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                duration = (localtime() - code_instance.created).total_seconds()
                if duration < 121:
                    user = User.objects.create_user(phone_number=sessions['phone_number'], email=sessions['email'],
                                            full_name=sessions['full_name'], password=sessions['password'])
                    login(request, user)
                    code_instance.delete()
                    messages.success(request, 'You register successfully', 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'The code expired', 'danger')
                    return redirect('accounts:register_verify_code')
            else:
                messages.error(request, 'The code is wrong', 'danger')
                return redirect('accounts:register_verify_code')
        else:
            return redirect('home:home')

class RegisterResendCodeView(View):
    def get(self, request):
        phone = request.session['user_registeration_info']['phone_number']                
        code_instance = OTPcode.objects.filter(phone_number=phone)
        if code_instance:
            code_instance.delete()
        create_otp(request, phone)
        return redirect('accounts:register_verify_code')
    
class UserLoginView(View):
    class_form = UserLoginForm

    def get(self, request):
        form = self.class_form
        context = {'form':form}
        return render(request, 'accounts/user_login.html', context)

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_login_info'] = {
                'phone_number': cd['phone_number'],
                'password': cd['password'],
            }
            create_otp(request, cd['phone_number'])
            return redirect('accounts:login_verify_code')

class UserLoginVerifyCodeView(View):
    def get(self, request):
        form = VerifyCodeForm
        return render(request, 'accounts/login_verify_code.html', {'form':form})

    def post(self, request):
        form = VerifyCodeForm(request.POST)
        session = request.session['user_login_info']
        code_instance = OTPcode.objects.filter(phone_number=session['phone_number']).order_by('-created')[0]
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                duration = (localtime() - code_instance.created).total_seconds()
                if duration < 121:
                    user = authenticate(request, username=session['phone_number'], password=session['password'])
                    if user:
                        code_instance.delete()
                        login(request, user)
                        messages.success(request, 'You login successfully', 'success')
                        return redirect('home:home')
                    else:
                        messages.error(request, 'incorre phone number or password', 'danger')
                        return redirect('accounts:user_login')
                else:
                    messages.error(request, 'The code expired', 'danger')
                    return redirect('accounts:login_verify_code')
            else:
                messages.error(request, 'The code is wrong', 'danger')
                return redirect('accounts:login_verify_code')
        else:
            return redirect('home:home')
        
class LoginResendCodeView(View):
    def get(self, request):
        phone = request.session['user_login_info']['phone_number']
        code_instance = OTPcode.objects.filter(phone_number=phone)
        if code_instance:
            code_instance.delete()
        create_otp(request, phone)
        return redirect('accounts:login_verify_code')
        
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')