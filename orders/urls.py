from django.urls import path
from orders import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.AddToCartView.as_view(), name='add_cart'),
    path('cart/remove/<int:product_id>', views.RemoveFromCartView.as_view(), name='remove_cart'),
    path('create/',views.OrderCreateView.as_view(), name='create_order'),
    path('details/<int:order_id>', views.OrderDetailsView.as_view(), name='order_details'),
    path('pay/<int:order_id>', views.OrderPayView.as_view(), name='pay_order'),
    path('verufy/', views.VerifyOrderView.as_view(), name='verify_order'),
    path('apply_coupon/<int:order_id>', views.ApplyCouponView.as_view(), name='apply_coupon'),
    
]