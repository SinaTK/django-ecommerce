from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product

class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products':products}
        return render(request, 'home/index.html', context)
    
class DetailsView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, pk=id, slug=slug)
        context = {'product': product}
        return render(request, 'home/details_page.html', context)