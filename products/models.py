from django.db import models

from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    TYPE_CHOICES = (
        ('featured', 'Featured'),
        ('trending', 'Trending'),
        ('carousel', 'Carousel'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bulk_pirce = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/')
    instock = models.BooleanField(default=True)  # Indicates if the product is in stock
    quantity_in_stock = models.PositiveIntegerField(default=0)  # Quantity available in stock
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class Checkout(models.Model):
    PAYMENT_CHOICES = [
        ('delivery', 'Payment for delivery'),
        ('pickup', 'Picking up in shop'),
        ('lay_buy', 'Paying a fraction (lay buy)'),
        ('pay_in_shop', 'Pay the complete money in shop physically'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    cart_items = models.JSONField()  # Now it will store only product IDs and quantities
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='delivery')  # Payment status field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for {self.user.email} at {self.created_at}"

    def calculate_total_price(self):
        total = 0
        for item in self.cart_items:
            try:
                # Fetch the product by its ID
                product = Product.objects.get(id=item['id'])

                # Determine the price based on the bulk option
                price = product.bulk_pirce if item.get('bulk', False) else product.price

                # Get the quantity, default to 1 if not provided
                quantity = item.get('quantity', 1)

                # Add the total price for this item
                total += float(price) * quantity
            except Product.DoesNotExist:
                continue  # Skip invalid product IDs
            except KeyError:
                continue  # Skip items with missing 'id' or 'bulk'
        return total

    
    
class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('payed', 'Payment made'),
        ('unpayed', 'No payment made'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_pay')
    items = models.JSONField() 
    orderId = models.CharField(max_length=100) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='unpayed')  # Payment status field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.user.email} at {self.created_at}"

    def calculate_total_price(self):
        total = 0
        for item in self.items:
            try:
                # Fetch the product by its ID
                product = Product.objects.get(id=item['id'])

                # Determine the price based on the bulk option
                price = product.bulk_pirce if item.get('bulk', False) else product.price

                # Get the quantity, default to 1 if not provided
                quantity = item.get('quantity', 1)

                # Add the total price for this item
                total += float(price) * quantity
            except Product.DoesNotExist:
                continue  # Skip invalid product IDs
            except KeyError:
                continue  # Skip items with missing 'id' or 'bulk'
        return total

    def update_payment_status(self, status='payed'):
        """
        Updates the payment status of the order.
        """
        self.status = status
        self.save()


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings', blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    review = models.TextField(blank=True, null=True)  # Optional review text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Admin_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)

    class Meta:
        unique_together = ('product', 'user')  # Ensures a user can rate a product only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} {self.rating}/5"
    

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"


class AboutUs(models.Model):
    company_name = models.CharField(max_length=255, default="Your Company Name")
    description = models.TextField(
        default="""Welcome to One-Stop Afroshop, an African shop in Germany dedicated 
        to bringing the vibrant and diverse flavors of Africa right to your doorstep. 
        We specialize in offering a wide range of authentic African products, from 
        traditional food ingredients to beauty and skincare products that celebrate 
        the rich cultures and heritage of the African continent.

        Our mission is to connect the African diaspora in Germany with the products 
        they love and miss from home. Whether you're craving a taste of home with 
        our diverse range of African food products or looking for high-quality 
        cosmetics made with natural African ingredients, we've got something for 
        everyone.

        We are passionate about sharing the essence of African culture through our 
        products, offering you a one-stop shop for all things African. We pride 
        ourselves on quality, authenticity, and a deep commitment to customer 
        satisfaction. As we continue to grow, we aim to expand our product range 
        and provide even more opportunities to experience the best of Africa 
        right here in Germany.
        """
    )
    description_de = models.TextField(
        default="""Willkommen bei One-Stop Afroshop, einem afrikanischen Geschäft in Deutschland, 
        das sich darauf spezialisiert hat, die lebendigen und vielfältigen Aromen Afrikas direkt zu Ihnen nach Hause zu bringen. 
        Wir bieten eine breite Palette authentischer afrikanischer Produkte an, von traditionellen Lebensmitteln bis hin zu 
        Schönheits- und Hautpflegeprodukten, die die reiche Kultur und das Erbe des afrikanischen Kontinents feiern.

        Unsere Mission ist es, die afrikanische Diaspora in Deutschland mit den Produkten zu verbinden, 
        die sie lieben und von zu Hause vermissen. Ob Sie sich nach einem Stück Heimat sehnen 
        mit unserer vielfältigen Auswahl an afrikanischen Lebensmitteln oder nach hochwertigen Kosmetika 
        suchen, die mit natürlichen afrikanischen Inhaltsstoffen hergestellt wurden – wir haben für jeden etwas dabei.

        Wir sind leidenschaftlich darum bemüht, das Wesen der afrikanischen Kultur durch unsere Produkte zu teilen, 
        und bieten Ihnen ein One-Stop-Shop für alles, was mit Afrika zu tun hat. Wir legen großen Wert auf Qualität, Authentizität 
        und ein tiefes Engagement für die Zufriedenheit unserer Kunden. Während wir weiter wachsen, 
        wollen wir unser Produktsortiment erweitern und noch mehr Möglichkeiten bieten, das Beste aus Afrika hier in Deutschland zu erleben.
        """
    )

    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)  # Added About Us image field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us Entries"



class RelatedProductImages(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='related_images')
    image = models.ImageField(upload_to='related_product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Related image for {self.product.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Related Product Image"
        verbose_name_plural = "Related Product Images"
