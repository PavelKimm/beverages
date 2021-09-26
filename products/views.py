import decimal
import math

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from products.models import Product
from products.serializers import ProductSerializer


class ProductListView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def get_order_total_price(request):
    total_price = 0
    product_codes = request.query_params.get('product_codes')
    if not product_codes:
        return Response({"message": "Product codes weren't provided."}, status=HTTP_400_BAD_REQUEST)
    product_codes = product_codes.split()
    required_products = Product.objects.filter(code__in=product_codes).values('code', 'price')
    # getting product prices to reduce queries to db
    product_prices = {}
    for product in required_products:
        product_prices[product['code']] = product['price']
    # getting product quantities
    products_count = {}
    for code in product_codes:
        if code in products_count:
            products_count[code] += 1
        else:
            products_count[code] = 1
    # getting total price with some rules
    for product_code, product_count in products_count.items():
        if product_code not in product_prices:
            return Response({"message": f"Invalid product code ({product_code})."}, status=HTTP_400_BAD_REQUEST)
        if product_code == 'PC' and product_count >= 3:
            discount = decimal.Decimal('0.2')
            total_price += (1 - discount) * product_prices[product_code] * product_count
        elif product_code == 'CC':
            total_price += product_prices[product_code] * math.ceil(product_count / 2)
        else:
            total_price += product_prices[product_code] * product_count
    return Response(f'${round(total_price, 2)}', status=HTTP_200_OK)
