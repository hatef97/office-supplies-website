from django.db import models
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self):
        return self.name



class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        permissions = [
            ('send_private_email', 'Can send private email to user by the button'),
        ]



class PageContent(models.Model):
    page_name = models.CharField(max_length=255, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.page_name



class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True)

    def __str__(self):
        return self.name



class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
