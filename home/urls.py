from django.urls import path, include
from home import views

app_name='home'

bucket_urls = [
    path('',views.BucketHome.as_view(), name='bucket_home'),
    path('delete-bucket-obj/<str:key>', views.DeleteBucketObject.as_view(), name='delete_bucket_obj'),
    path('download-bucket-obj/<str:key>', views.DownloadBucketObject.as_view(), name='download_bucket_obj'),
    path('upload-bucket-obj', views.UploadBucketObject.as_view(), name='upload_bucket_obj'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>', views.HomeView.as_view(), name='category_products'),
    path('detials/<int:id>/<slug:slug>', views.DetailsView.as_view(), name='details_page'),
    path('bucket/', include(bucket_urls))
]