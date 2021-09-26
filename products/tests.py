from django.test import TestCase
from django.urls import reverse

from products.models import Product


class TotalPriceTestCase(TestCase):
    def setUp(self):
        Product.objects.create(code='CC', name='Coca-Cola', price=1.50)
        Product.objects.create(code='PC', name='Pepsi Cola', price=2.00)
        Product.objects.create(code='WA', name='Water', price=0.85)

    def test_total_price(self):
        response = self.client.get(f"{reverse('get-total-price')}?product_codes=CC PC WA")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '$4.35')

        response = self.client.get(f"{reverse('get-total-price')}?product_codes=CC PC CC CC")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '$5.00')

        response = self.client.get(f"{reverse('get-total-price')}?product_codes=PC CC PC WA PC CC")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '$7.15')
