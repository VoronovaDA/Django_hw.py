from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, default=[])

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'products']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for product in positions:
            StockProduct.objects.create(stock_id=stock.id,
                                        product_id=product['product'].id,
                                        quantity=product['quantity'],
                                        price=product['price'])
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions', [])
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, product=position['product'], defaults={'quantity': position['quantity'], 'price': position['price']})
        return stock
