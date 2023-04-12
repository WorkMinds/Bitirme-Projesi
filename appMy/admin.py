from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('title','id','user','category','price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('title','id','slug')

@admin.register(ProductStok)
class ProductStokAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('product','id','stok')

@admin.register(ProductImg)
class ProductImgAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('product','id','image')

@admin.register(Shopbasket)
class ShobbasketAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('user','product_basket','price_total','amount','id')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin View for '''
    list_display = ('user','product','star','date_now','id')

admin.site.register(UserInfo)


    

     
 