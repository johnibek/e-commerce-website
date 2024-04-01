from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('products/<int:pk>', views.product_detail, name='product'),
    path('category/<slug:slug>', views.category_detail, name='category'),
    path('category_summary', views.category_summary, name='category_summary'),
    path('load/', views.load_products),
    path('search/', views.search, name='search'),
]