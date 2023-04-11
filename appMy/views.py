from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.db.models import Q

# Create your views here.

def index(request):
    products = ProductStok.objects.all()[:4]
    product = ProductStok.objects.all()[:1]
    context={
        "products":products,
        "product":product
    }
    return render(request,'index.html',context)

def Products(request):
    return render(request,'products.html')

def About(request):
    context={}
    return render(request,'about.html',context)

def Contact(request):
    context={}
    return render(request,'contact.html',context)

def Shop(request):
    products = ProductStok.objects.all()

    query = request.GET.get("query")
    if query:
        products=products.filter(
            Q(product__title__icontains=query) |
            Q(product__brand__icontains=query) |
            Q(product__slug__icontains=query)
                
            )
    
    context={
        "products":products,
    }
    return render(request,'shop.html',context)

def ShopDetail(request,slug):
    product = get_object_or_404(ProductStok,product__slug=slug)
    book = Product.objects.get(slug=slug)
    comments = Comment.objects.filter(product=book).order_by("-star")
    puan = 0
    if request.method == "POST":
        submit = request.POST.get("submit")
        if submit == "buy":
            try:
                amount = int(request.POST.get("amount"))
            except:
                return redirect('/ShopDetail/'+ slug + '/')
            
            if amount > 0:
                price_total = product.product.price * amount
                shopprod = Shopbasket.objects.filter(user=request.user,product_basket=product)

                if shopprod.exists():
                    shopprod = shopprod.get()
                    shopprod.amount += amount
                    shopprod.price_total += price_total
                    shopprod.save()
                else:

                    shopb = Shopbasket(user = request.user,
                                    product_basket=product,
                                    price_total=price_total,
                                    amount=amount)
                    shopb.save()
            return redirect('/ShopDetail/'+ slug + '/')
        elif submit == "comment":
            text = request.POST.get("text")
            try:
                star = int(request.POST.get("star"))
            except:
                return redirect('/ShopDetail/'+ slug + '/')
            
            
            comment = Comment(user=request.user,product=book,text=text,star=star)
            comment.save()

            for i in comments:
                puan += i.star

            book.stars = round(puan/len(comments),1)
            book.save()

           
            
            return redirect('/ShopDetail/'+ slug + '/')

        
        

    context={
        "comments": comments,
        "product":product,
    }
    return render(request,'single-product.html',context)

def ShopBasket(request):
    
    shopbasket = Shopbasket.objects.filter(user=request.user)
    toplam = 0
    for i in shopbasket:
        toplam += i.price_total

    if request.method == "POST":
        for k,v in dict(request.POST).items():
          if k != "csrfmiddlewaretoken":
            try:
                v[0] = int(v[0])
            except:
                return redirect ('ShopBasket')
            shopb =shopbasket.get(id=k[6:])
            if v[0] == "0":
                shopb.delete()
            elif v[0] > 0:
                shopb.amount = v[0]
                shopb.price_total = shopb.product_basket.product.price * int(v[0])
                shopb.save()
            else:
                return redirect ('ShopBasket')
                
        return redirect('ShopBasket') 

    context={
        "shopbasket":shopbasket,
        "toplam":toplam,
    }
    return render(request,'user/shop-basket.html',context)

def ShopBasketDelete(request,sid):

    shopbasket = Shopbasket.objects.get(id=sid)
    shopbasket.delete()
    return redirect('ShopBasket')


# USER 
def loginUser(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        harfet = False
        for harf in username:
            if harf == "@":
                harfet = True
        if username[-4:] == ".com" and harfet:
            try:
                username = User.objects.get(email=username).username
            except:
                messages.warning(request,"Bu email'e ait bir kullanıcı yok!")
                return redirect('loginUser')



        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.warning(request, "Kullanıcı adı veya şifreyi yanlış girdiniz!")
            return redirect('loginUser')

    return render(request,'user/login.html')

def logoutUser(request):
    logout(request)
    return redirect('index')

def registerUser(request):

    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        harfup = False
        harfnum = False
        if password1 == password2:

            for harf in password1:
                if harf.isupper():
                    harfup = True
                if harf.isnumeric():
                    harfnum = True

            if harfup and harfnum and len(password1)>=6:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username = username,
                                                        password = password1,
                                                        email = email,
                                                        first_name = name,
                                                        last_name = surname)
            
                        user.save()
                        return redirect('loginUser')
                    else:
                        messages.warning(request,"Aynı email'e sahip bir kullanıcı mevcut!")
                        return redirect('registerUser')
                else:
                    messages.warning(request,"Bu kullanıcı adı alınmış!")
                    return redirect('registerUser')
            else:
                messages.warning(request,"Şifrede en az bir büyük harf olmalı!")
                messages.warning(request,"Şifrede en az bir sayı olmalı!")
                messages.warning(request,"Şifre en az 6 karakterden oluşmalı!")
                return redirect('registerUser')
        else:
            messages.warning(request,"Şifreler uyumlu değil!")
            return redirect('registerUser')

    return render(request, 'user/register.html')

def changePassword(request):
    
    if request.method == "POST":
        password = request.POST["password"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        user = User.objects.get(username= request.user)
        
        if user.check_password(password):
            if password2 == password1:
                user.set_password(password1)
                user.save()
                logout(request)
                return redirect('loginUser')
            else:
                messages.warning(request,"Yeni şifreniz her iki sekmede aynı olmalı!!")
                return redirect('changePassword')
        else:
            messages.warning(request,"Eski şifrenizi yanlış girdiniz!")
            return redirect('changePassword')
    
    return render(request, 'user/change-password.html')

def profilUser(request):
    context= {}

    user = User.objects.get(username=request.user)

    context.update({"user":user})
    return render(request,'user/profil.html',context)
