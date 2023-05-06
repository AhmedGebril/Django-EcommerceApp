"""
URL configuration for projectname project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from Users import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('create/user',views.Register),
    path('login',views.login),
    path('users/admin/getusers', views.AdminUserListView.as_view(), name='get_users'),
    path('users/admin/<int:pk>', views.AdminUserDetailView.as_view(), name='user_detail'),
    path('get_all_products',views.ProductList.as_view(),name='get all products'),
    path('get_product/<int:pk>',views.ProductDetail.as_view(),name='get_certain_product'),
    path('createReview',views.ProductReviewCreateAPIView.as_view(),name='Create_product_review'),
    path('add_order_item',views.addOrderItems,name='add_order_items'),

    ]


