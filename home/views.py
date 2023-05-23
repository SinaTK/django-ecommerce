from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Product, Category
from home import tasks
from django.contrib import messages
from home.forms import UploadObj
from utils import IsAdminUserMixin


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.all()
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            cat = Category.objects.get(slug=category_slug)
            products = products.filter(category=cat)
        
        context = {'products':products, 'categories':categories}
        return render(request, 'home/index.html', context)
    
class DetailsView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, pk=id, slug=slug)
        context = {'product': product}
        return render(request, 'home/details_page.html', context)
    
class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'
 
    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        context = {'objects':objects}
        return render(request, self.template_name, context)
    

class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_bucket_object_task.delay(key)
        messages.success(request, 'The object will be delete soon.', 'info')
        return redirect('home:bucket_home')
    
class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_bucket_object_task.delay(key)
        messages.success(request, 'The object will be download soon.', 'info')
        return redirect('home:bucket_home')

class UploadBucketObject(IsAdminUserMixin, View):
    class_form = UploadObj
    template_name = 'home/upload_obj.html'

    def get(self, request):
        form = self.class_form
        return render(request, self.template_name, {'form':form})


    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data    
            if not cd['bucket_file_name']:
                cd['bucket_file_name'] = cd['file_name'].split('/')[-1]
            tasks.upload_bucket_object_task.delay(file_name=cd['file_name'], bucket_file_name=cd['bucket_file_name'])
            messages.success(request, 'Your file will be upload soon.', 'info')
            return redirect('home:bucket_home')
        else:
            return render(request, self.template_name, {'form':form})