"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/ <str:cat>', views.product, name='product'),
    path('pbdetail/<int:pk>', views.pbdetail, name='pbdetail'),
    path('addtowishlist/<int:pk>', views.addtowishlist, name='addtowishlist'),
    path('product-detail/', views.product_detail, name='product-detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('removewishlist/<int:pk>', views.removewishlist, name='removewishlist'),
    # path('shoping-cart/<int:pk>', views.shoping, name='shoping-cart'),
    # path('Remove-shoping-cart/<int:pk>', views.Remove_cart, name='Remove-shoping-cart'),
    path('blog/', views.blog, name='blog'),
    path('blog-detail/', views.blogdetail, name='blog-detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('fpass/', views.fpass, name='fpass'),
    path('otp/', views.otp, name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('profile/',views.profile,name='profile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('sindex/',views.sindex,name='sindex'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('viewproduct/ <str:cat>/',views.viewproduct,name='viewproduct'),
    path('sprofile/',views.sprofile,name='sprofile'),
    path('schangepassword/',views.changepassword,name='schangepassword'),
    path('pdetail/ <int:pk>',views.pdetail,name='pdetail'),
    path('pedit/ <int:pk>',views.pedit,name='pedit'),
    path('pdelete/ <int:pk>',views.pdelete,name='pdelete'),
    path('shoping_cart/', views.shoping_cart, name='shoping_cart'),
    path('add_to_cart/ <int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/ <int:pk>/', views.delete_cart, name='delete_cart'),
    path('change_quantity/ <int:pk>/', views.change_quantity, name='change_quantity'),
    path('order_details', views.order_details, name='order_details'),
    path('check_out/', views.check_out, name='check_out'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
]
