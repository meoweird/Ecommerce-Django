from django.urls import path

from item import views

urlpatterns = [
    path('list', views.ItemListView.as_view(), name='item-list'),
    path('detail', views.ItemDetailView.as_view(), name='item-detail'),
    path('create', views.ItemCreateView.as_view(), name='item-create'),
    path('category/list', views.CategoryListView.as_view(), name='category-list'),
    path('category/detail', views.CategoryDetailView.as_view(), name='category-detail'), 
    path('category/create', views.CategoryCreateView.as_view(), name='category-create'),
]
