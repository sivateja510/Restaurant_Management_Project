# restaurant/urls.py
from django.urls import path
from . import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'menuitems', views.MenuItemViewSet)
router.register(r'orderitems', views.OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('menu', views.menu_list, name='menu_list'),
    path('menuchef/', views.menu_list_chef, name='menu_lists'),
    path('update/<int:pk>/', views.update_menu_item, name='update_menu_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/update/', views.update_order, name='update_order'),
    path('Accept_orders/', views.accept_order, name='accept_order'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('create_order/', views.create_order, name='create_order'),
    path('', views.user_login, name='user_login'), 
    path('logout/', views.logout_view, name='logout'),
    path('myorders/', views.myorders, name='myorders'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('print_order_history/', views.print_order_history, name='print_order_history'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('clear-all-orders/', views.clear_all_orders, name='clear_all_orders'),
    
    
]

