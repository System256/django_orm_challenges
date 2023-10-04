from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    

class Laptop(models.Model):
    class Meta:
        verbose_name = "laptop"
        verbose_name_plural = "laptops"
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    brand = models.CharField(
        max_length=256,
        choices=[('AS', 'Asus'), ('AE', 'Apple'), ('LO', 'Lenovo'), ('DL', 'Dell')],
    )
    release_year = models.PositiveSmallIntegerField()
    amount_ram_mb = models.PositiveSmallIntegerField(help_text='Capacity in MB')
    amount_hdd_mb = models.PositiveSmallIntegerField(help_text='Capacity in MB')
    price = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f'\nBrand: {self.brand}\n'
            f'Release year: {self.release_year}\n'
            f'Price: {self.price}\n'
            f'Quantity in stock: {self.quantity_in_stock}\n'
            f'Added date: {self.created_at}\n'
        )
    

class Post(models.Model):
    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    title = models.CharField(max_length=256)
    text = models.CharField(max_length=6000)
    authors_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=5,
        choices=[('pub', 'published'), ('unpub', 'unpublished'), ('ban', 'banned')],
        default='pub',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published_in = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=2,
        choices=[('1', 'Animals'), ('2', 'Cars'), ('3', 'Programming'), ('4', 'Monitors')],
        null=True,
    )

    def __str__(self):
        return (
            f'\nTitle: {self.title}\n'
            f'Status: {self.status}\n'
            f'Created at: {self.created_at}\n'
            f'Category: {self.category}\n'
        )