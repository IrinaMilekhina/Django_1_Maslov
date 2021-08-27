from django.urls import path

from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders_list'),
    path('read/<int:pk>/', views.OrderItemRead.as_view(), name='order_read'),
    path('update/<int:pk>/', views.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', views.OrderItemDelete.as_view(), name='order_delete'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
    path('forming/complete/<int:pk>/', views.order_forming_complete, name='order_forming_complete'),
    path('order_item_price/<int:pk>/', views.product_price)
]
