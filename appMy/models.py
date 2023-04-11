from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    slug = models.SlugField(("Slug Kategori"),blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), max_length=50)
    brand = models.CharField(("Yayınevi"),blank=True, max_length=50)
    writer = models.CharField(("Yazar"),blank=True, max_length=50)
    image = models.ImageField(("Fotoğraf"), upload_to='media')
    text = models.TextField(("Açıklama"),max_length=1000)
    detail = models.TextField(("Özellikler"),blank=True)
    price = models.FloatField(("Fiyat"),default=0)
    stars = models.FloatField(("Puan"),default=0)
    slug = models.SlugField(("Slug Title"),blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
      return self.title 
    
class ProductImg(models.Model):
    product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE)
    image = models.ImageField(("Resim"), upload_to="product")

    def __str__(self):
      return self.product.title

class ProductStok(models.Model):
    product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE)
    images = models.ManyToManyField(ProductImg, verbose_name=("Ürün Resimleri"),blank=True)
    stok = models.IntegerField(("Ürün Stok Sayısı"),default=0)

    def __str__(self):
      return self.product.title + " || " + self.product.category.title + " || " + self.product.writer

class Shopbasket(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    product_basket = models.ForeignKey(ProductStok, verbose_name=("Sepetteki Ürün"), on_delete=models.CASCADE)
    price_total = models.FloatField(("Toplam Fiyat"),default=0)
    amount = models.IntegerField(("Adet"),default=0)

    def __str__(self):
      return self.product_basket.product.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE)
    text = models.TextField(("Yorum"),max_length=800)
    date_now = models.DateTimeField(("Tarih ve Saat"), auto_now_add=True)
    star = models.IntegerField(("Yorum Puanı"),default=5)
