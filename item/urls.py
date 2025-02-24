from django.urls import path

from item import views

urlpatterns = [
    path('list', views.ItemListView.as_view(), name='item-list'),
    path('detail', views.ItemDetailView.as_view(), name='item-detail'),
    path('category/list', views.CategoryListView.as_view(), name='category-list'),
    path('create', views.ItemPostView.as_view(), name='item-create'),
    path('category/create', views.CategoryPostView.as_view(), name='category-create'),
]
