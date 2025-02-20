# products/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from user.models import User
from .models import AboutUs, Category, Checkout, Payment, Product, ProductRating
from .serializers import AboutUsSerializer, CategorySerializer, CheckoutSerializer, ContactUsSerializer, EnrichedCheckoutSerializer, EnrichedPaymentSerializer, PaymentSerializer, ProductRatingSerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny  # Import AllowAny permission class

# Custom Pagination Class
class ProductPagination(PageNumberPagination):
    page_size = 20  # You can adjust the page size here
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'type']  # Allow filtering by category and type
    search_fields = ['name', 'description']  # Enable searching by product name or description
    permission_classes = [AllowAny]  # Bypass authorization for all actions

    # Fetches all products
    @action(detail=False, methods=['get'], url_path='getProducts')
    def get_products(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        
        # Manually create a response structure similar to paginated data
        response_data = {
            "count": len(products),
            "next": None,  # No next page
            "previous": None,  # No previous page
            "results": serializer.data,  # All products
        }
        return Response(response_data)


    # Fetches a single product by its ID
    @action(detail=True, methods=['get'], url_path='getSingleProduct')
    def get_single_product(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    # Filters products based on a category filter
    @action(detail=False, methods=['get'], url_path='filterProducts')
    def filter_products(self, request):
        category_filter = request.query_params.get('category', None)
        products = self.get_queryset()
        if category_filter:
            products = products.filter(category__id=category_filter)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Fetches products based on the carousel type
    @action(detail=False, methods=['get'], url_path='getCarousalProducts')
    def get_carousal_products(self, request):
        products = self.get_queryset().filter(type='carousel')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        response_data = {
            "count": len(products),
            "next": None,  # No next page
            "previous": None,  # No previous page
            "results": serializer.data,  # All products
        }
        return Response(response_data)

    # Fetches featured products
    @action(detail=False, methods=['get'], url_path='getFeaturedProducts')
    def get_featured_products(self, request):
        products = self.get_queryset().filter(type='featured')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Fetches trending products
    @action(detail=False, methods=['get'], url_path='getTrendProducts')
    def get_trend_products(self, request):
        products = self.get_queryset().filter(type='trending')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        response_data = {
            "count": len(products),
            "next": None,  # No next page
            "previous": None,  # No previous page
            "results": serializer.data,  # All products
        }
        return Response(response_data)
    
    
    # Submit a product rating
    @action(detail=True, methods=['post'], url_path='submitRating')
    def submit_rating(self, request, pk=None):
        product = self.get_object()

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the rating from the request
        rating = request.data.get('rating')

        if rating is None:
            return Response({'detail': 'Rating is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use update_or_create to either update an existing rating or create a new one
        obj, created = ProductRating.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating}  # This will update the rating if it exists, or create a new rating if it doesn't
        )

        if created:
            # If the rating was created
            return Response({'detail': 'Rating submitted successfully.', 'rating': obj.rating}, status=status.HTTP_201_CREATED)
        else:
            # If the rating was updated
            return Response({'detail': 'Rating updated successfully.', 'rating': obj.rating}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['get'], url_path='getProductRating')   
    def get_product_rating(self, request, pk=None):
        try:
            # Filter ProductRating by product_id (pk in this case)
            ratings = ProductRating.objects.filter(product_id=pk)
            
            # Check if there are any ratings
            if ratings.exists():
                # First check for the Admin rating
                product_rating = ratings.first()  # Get the first rating

                if product_rating.Admin_rating:
                    return Response({"rating": product_rating.Admin_rating})
                
                # If Admin rating is not set, calculate average rating
                avg_rating = sum([rating.rating for rating in ratings]) / len(ratings)
                return Response({"rating": round(avg_rating, 2)})
            
            # If no ratings exist, return a default value (could be 0 or None)
            return Response({"rating": 0})

        except Exception as e:
            # Return an error response in case of any exception
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']  # Restrict to read-only operations
    permission_classes = [AllowAny]  # Bypass authorization for all actions

    # Custom action to handle 'getCategories' route
    @action(detail=False, methods=['get'], url_path='getCategories')
    def get_categories(self, request):
        categories = self.queryset.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CheckoutView(views.APIView):
    
    def post(self, request, *args, **kwargs):
        # Check if the user is authenticated
        print("Authenticated User:", request.data)

        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Access cartItems correctly using get method to avoid key errors
        cart_items = request.data.get('cartItems', [])
        print("Cart items received:", cart_items)

        # Prepare the data to be passed to the serializer
        data = {
            'userId': request.user.id,  # Pass authenticated user's ID
            'cartItems': cart_items      # Pass the cart items
        }

        # Pass the data to the serializer
        serializer = CheckoutSerializer(data=data)
        if serializer.is_valid():
            checkout = serializer.save()  # This will automatically calculate the total_price
            return Response({
                'message': 'Checkout successful',
                'checkout': CheckoutSerializer(checkout).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        user = User.objects.get(pk=user.id)
        print(user.id)
        checkouts = Checkout.objects.filter(user__id=user.id)

        if not checkouts.exists():
            return Response({'message': 'No checkouts found for this user'})

        serializer = EnrichedCheckoutSerializer(checkouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckoutItemDeleteView(APIView):
    def delete(self, request, checkout_id, item_id, *args, **kwargs):
        try:
            # Fetch the checkout instance
            checkout = Checkout.objects.get(id=checkout_id, user=request.user)
        except Checkout.DoesNotExist:
            return Response({'detail': 'Checkout not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        # Find the item in the cart and remove it
        item_to_remove = None
        for item in checkout.cart_items:
            if item['id'] == item_id:
                item_to_remove = item
                break

        if item_to_remove:
            checkout.cart_items.remove(item_to_remove)
            checkout.total_price = checkout.calculate_total_price()
            checkout.save()
            return Response({
                'message': 'Item removed from checkout',
                'checkout': CheckoutSerializer(checkout).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Item not found in the checkout'}, status=status.HTTP_404_NOT_FOUND)
        


class CheckoutDeleteView(APIView):
    def delete(self, request, checkout_id, *args, **kwargs):
        try:
            # Fetch the checkout instance
            checkout = Checkout.objects.get(id=checkout_id, user=request.user)
        except Checkout.DoesNotExist:
            return Response({'detail': 'Checkout not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the entire checkout, including all items
        checkout.delete()

        return Response({
            'message': 'Checkout and all items have been deleted'
        }, status=status.HTTP_204_NO_CONTENT)
        
class PaymentView(views.APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        items = request.data.get('items', [])
        orderId = request.data.get('orderId')

        data = {
            'userId': request.user.id,
            'items': items,
            'orderId': orderId,
        }

        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()  # This will automatically calculate the total_price
            return Response({
                'message': 'Order successful',
                'order': PaymentSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        order = Payment.objects.filter(user=user)

        if not order.exists():
            return Response({'message': 'No checkouts found for this user'})

        serializer = EnrichedPaymentSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id, *args, **kwargs):
        try:
            payment = Payment.objects.get(id=order_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({'detail': 'Checkout not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        payment.delete()
        return Response({'message': 'Checkout and all items have been deleted'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        """
        Updates the payment status of a specific order to 'payed'.
        """
        order_id = kwargs.get('order_id')
        print(order_id)
        try:
            payment = Payment.objects.get(id=order_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({'detail': 'Payment not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        payment.update_payment_status('payed')
        return Response({'message': 'Payment status updated to paid.'}, status=status.HTTP_200_OK)



class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]

    # Custom actions (optional, depending on your needs)
    @action(detail=False, methods=['get'])
    def get_about_us(self, request):
        about_us = AboutUs.objects.first()  # Assuming only one "About Us" entry
        if about_us:
            serializer = self.get_serializer(about_us)
            return Response(serializer.data)
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    
class ContactUsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Your message has been received. We'll get back to you soon!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)