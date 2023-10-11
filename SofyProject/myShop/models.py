from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):

    name = models.CharField("category", max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    product_name = models.CharField("product name", max_length=100)
    category = models.ForeignKey("Category", verbose_name="category", on_delete=models.CASCADE)
    price = models.IntegerField("product price", default=0)
    desc = models.CharField("description", max_length=300)
    image = models.ImageField("image", upload_to="images/images", height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Customer(models.Model):

    user = models.OneToOneField(User, verbose_name="customer", on_delete=models.CASCADE)
    phone = models.CharField("phone number", max_length=11)
    address1 = models.CharField("address", max_length=200, default="")
    address2 = models.CharField("address", max_length=200, default="")
    city = models.CharField("city", max_length=100, default="")
    state = models.CharField("state", max_length=100, default="")
    zip_code = models.CharField("zip code", max_length=100, default="")

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})



class Order(models.Model):

    order_id = models.AutoField("order id", primary_key=True)
    items_json = models.CharField("order items", max_length=5000)
    amount = models.IntegerField("quantity", default=0)
    customer = models.ForeignKey("Customer", verbose_name="customer", on_delete=models.CASCADE)
    oid = models.CharField("oid", max_length=150, blank=True)
    amountpaid = models.CharField("amount paid", max_length=500, blank=True, null=True)
    paymentstatus = models.CharField("payment status", max_length=20, blank=True)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
