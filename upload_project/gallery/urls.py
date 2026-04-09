from django.urls import path
from . import views
urlpatterns = [path('upload/', views.upload_view, name='upload'), path('display/', views.display_view, name='display')]