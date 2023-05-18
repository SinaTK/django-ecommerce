from django.urls import path
from home import views

app_name='home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('detials/<int:id>/<slug:slug>', views.DetailsView.as_view(), name='details_page')
]