from django.urls import path

from products.views import ProductListView, ProductDetailView, get_order_total_price

urlpatterns = [
    path('', ProductListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),

    path('total/', get_order_total_price, name='get-total-price')
]
