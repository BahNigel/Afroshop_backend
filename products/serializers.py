from rest_framework import serializers

from user.models import User
from .models import AboutUs, Category, Checkout, ContactUs, Payment, Product, ProductRating, RelatedProductImages

class ProductSerializer1(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # Ensure the image URL is included

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer1(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        
        
class RelatedProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedProductImages
        fields = ['id', 'image', 'created_at']
        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    related_images = RelatedProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)
    cartItems = serializers.JSONField(write_only=True)

    class Meta:
        model = Checkout
        fields = ['userId', 'cartItems', 'total_price']

    def create(self, validated_data):
        user_id = validated_data.pop('userId')
        user = User.objects.get(id=user_id)
        cart_items = validated_data.pop('cartItems')

        checkout = Checkout.objects.create(user=user, cart_items=cart_items, **validated_data)
        checkout.total_price = checkout.calculate_total_price()
        checkout.save()

        return checkout
    
            
class PaymentSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)
    items = serializers.JSONField(write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'userId', 'items', 'orderId', 'total_price']

    def create(self, validated_data):
        user_id = validated_data.pop('userId')
        user = User.objects.get(id=user_id)

        checkout = Payment.objects.create(user=user, **validated_data)
        checkout.total_price = checkout.calculate_total_price()
        checkout.save()

        return checkout
    
class CartItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()


class EnrichedCheckoutSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Checkout
        fields = ['id', 'total_price', 'status', 'created_at', 'cart_items']

    def get_cart_items(self, obj):
        enriched_items = []
        for item in obj.cart_items:
            try:
                # Fetch the product based on item ID
                product = Product.objects.get(id=item['id'])
                
                # Get the 'bulk' field safely, default to None if it doesn't exist
                bulk = item.get('bulk', None)
                
                # Append the enriched item information
                enriched_items.append({
                    'product': ProductSerializer(product).data,
                    'quantity': item.get('quantity', 1),  # Default to 1 if quantity is missing
                    'bulk': bulk,
                })
            except Product.DoesNotExist:
                continue  # Skip if the product doesn't exist
            except KeyError:
                continue  # Skip if the 'id' or other keys are missing in the item

        return enriched_items

    
    
class EnrichedPaymentSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['id', 'orderId', 'total_price', 'status', 'created_at', 'items']

    def get_items(self, obj):
        enriched_items = []
        for item in obj.items:
            try:
                product = Product.objects.get(id=item['id'])
                bulk = item.get('bulk', None)
                enriched_items.append({
                    'product': ProductSerializer(product).data,
                    'quantity': item['quantity'],
                    'bulk': bulk
                })
            except Product.DoesNotExist:
                continue
        return enriched_items


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['product', 'rating']
        read_only_fields = ['user'] 
        
        
        
class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'company_name', 'description', 'description_de', 'location', 'latitude', 'longitude', 'email', 'phone', 'website', 'image', 'created_at']
        
        
        
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["name", "email", "subject", "message"]
