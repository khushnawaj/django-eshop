from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *


def home(request):
    data = Product.objects.all().order_by('id').reverse()[:6]
    return render(request, "index.html", {'data': data})


def shop(request, mc, sc, br):
    if mc == 'All' and sc == "All" and br == 'All':
        data = Product.objects.all().order_by('id').reverse()
    elif mc != 'All' and sc == "All" and br == 'All':
        data = Product.objects.filter(
            maincategory=Maincategory.objects.get(name=mc)).order_by('id').reverse()
    elif mc == 'All' and sc != "All" and br == 'All':
        data = Product.objects.filter(
            subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif mc == 'All' and sc == "All" and br != 'All':
        data = Product.objects.filter(
            brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif mc != 'All' and sc != "All" and br == 'All':
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif mc != 'All' and sc == "All" and br != 'All':
        data = Product.objects.filter(maincategory=Maincategory.objects.get(
            name=mc), brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif mc == 'All' and sc != "All" and br != 'All':
        data = Product.objects.filter(brand=Brand.objects.get(
            name=br), subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    else:
        data = Product.objects.filter(
            brand=Brand.objects.get(name=br),
            subcategory=Subcategory.objects.get(name=sc),
            maincategory=Maincategory.objects.get(name=mc)
        )

    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()

    return render(request, "shop.html", {'data': data, 'maincategory': maincategory, 'subcategory': subcategory, 'brand': brand, 'mc': mc, 'sc': sc, 'br': br})


def singleProduct(request, id):
    data = Product.objects.get(id=id)
    return render(request, "single-product.html", {'data': data})


# def loginPage(request):
#     if (request.method == "POST"):
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(username=username, password=password)
#             login(request,user)
#             return redirect("/profile")
#         except:
#             messages.error(request,"Invalid Username or Password!!!")

#     return render(request, "login.html")
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  # Use "Password" here

        # Use authenticate to handle password hashing and authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect("/profile")
        else:
            messages.error(request, "Invalid Username or Password!!!")

    return render(request, "login.html")


def logoutPage(request):
    logout(request)
    return redirect('/login')


def signupPage(request):
    if request.method == "POST":
        p = request.POST.get("password")
        cp = request.POST.get("cpassword")

        if p == cp:
            # Check if a user with the same username or email already exists
            if User.objects.filter(username=request.POST.get("username")).exists() or User.objects.filter(email=request.POST.get("email")).exists():
                messages.error(request, "Username or Email Already Registered")
            else:
                # Create and save User and Buyer objects
                user = User(username=request.POST.get("username"))
                user.set_password(p)
                user.email = request.POST.get("email")  # Set the email here
                user.save()

                b = Buyer(name=request.POST.get("name"), username=request.POST.get(
                    "username"), phone=request.POST.get("phone"), email=request.POST.get("email"))
                b.save()

                messages.success(
                    request, "Account created successfully. You can now log in.")
                return redirect("/login/")
        else:
            messages.error(
                request, "Password and Confirm Password Don't Match")

    return render(request, "signup.html")


@login_required(login_url='/login/')
def profilePage(request):
    user = User.objects.get(username=request.user)
    if (user.is_superuser):
        return redirect("/admin")
    else:
        buyer = Buyer.objects.get(username=user.username)

    return render(request, "profile.html", {'user': buyer})


# @login_required(login_url='/login/')
# def updateProfilePage(request):
#     user = User.objects.get(username=request.user)
#     if (user.is_superuser):
#         return redirect("/admin")
#     else:
#         buyer = Buyer.objects.get(username=user.username)
#         if(request.method == "POST"):
#             buyer.name = request.POST.get("name")
#             buyer.email = request.POST.get("email")
#             buyer.phone = request.POST.get("phone")
#             buyer.addressline1 = request.POST.get("addressline1")
#             buyer.addressline2= request.POST.get("addressline2")
#             buyer.addressline3 = request.POST.get("addressline3")
#             buyer.pin = request.POST.get("pin")
#             buyer.city = request.POST.get("city")
#             buyer.state = request.POST.get("state")
#             if(request.FILES.get("profile_picture")!=""):
#                 buyer.pic = request.FILES.get("profile_picture")
#             buyer.save()
#             return redirect("/profile")
#     return render(request, "update-profile.html", {'user': buyer})

@login_required(login_url='/login/')
def updateProfilePage(request):
    user = User.objects.get(username=request.user)

    # Check if the user is a superuser
    if user.is_superuser:
        # Log this action or provide a message
        return redirect("/admin")

    buyer = Buyer.objects.get(username=user.username)

    if request.method == "POST":
        buyer.name = request.POST.get("name")
        buyer.email = request.POST.get("email")
        buyer.phone = request.POST.get("phone")
        buyer.addressline1 = request.POST.get("addressline1")
        buyer.addressline2 = request.POST.get("addressline2")
        buyer.addressline3 = request.POST.get("addressline3")
        buyer.pin = request.POST.get("pin")
        buyer.city = request.POST.get("city")
        buyer.state = request.POST.get("state")

        # Check if a file is provided before updating the profile_picture field
        if request.FILES.get("profile_picture"):
            buyer.profile_picture = request.FILES.get("profile_picture")

        buyer.save()

        # Redirect to the correct profile page
        return redirect("/profile")

    return render(request, "update-profile.html", {'user': buyer})


# def addToCart(request, id):
#     cart = request.session.get('cart', None)
#     p = Product.objects.get(id=id)
#     if cart is None:
#         cart = { p.id,{'name': p.name, 'color': p.color, 'size': p.size,
#                 'price': p.finalprice, 'maincategory': p.maincategory, 'subcategory': p.subcategory, 'brand': p.brand}}
#     else:
#         if p.id in cart:
#             pass
#         else:
#             cart.setdefault({ p.id,{'name': p.name, 'color': p.color, 'size': p.size,
#                 'price': p.finalprice, 'maincategory': p.maincategory, 'subcategory': p.subcategory, 'brand': p.brand}})

#     request.session['cart'] = cart
#     request.session.set_expiry(60*60*24*45)
#     return redirect("/cart")


# FOR ADD TO CART PAGE

def addToCart(request, id):
    # cart = request.session.flush()
    cart = request.session.get('cart', None)
    p = Product.objects.get(id=id)

    if (cart is None):
        cart = {str(p.id): {
            'pid': p.id,
            'pic': p.pic1.url,
            'name': p.name,
            'color': p.color,
            'size': p.size,
            'price': p.finalprice,
            'qty': 1,
            'total': p.finalprice,
            'maincategory': p.maincategory.name,
            'subcategory': p.subcategory.name,
            'brand': p.brand.name,
        }}
    else:
        if (str(p.id) in cart):

            item = cart[str(p.id)]
            item['qty'] = item['qty']+1
            item['total'] = item['total']+item['price']
            cart[str(p.id)] = item

        else:
            cart.setdefault(str(p.id), {

                'pid': p.id,
                'pic': p.pic1.url,
                'name': p.name,
                'color': p.color,
                'size': p.size,
                'price': p.finalprice,
                'qty': 1,
                'total': p.finalprice,
                'maincategory': p.maincategory.name,
                'subcategory': p.subcategory.name,
                'brand': p.brand.name,
            }
            )

    request.session['cart'] = cart
    request.session.set_expiry(60*60*24*45)
    return redirect("/cart")


# FOR CARTPAGE


def cartPage(request):
    cart = request.session.get('cart', None)
    c = []
    total = 0
    shipping = 0
    if cart is not None:
        for value in cart.values():
            total = total + value['total']
            c.append(value)
        if (total < 1000):
            shipping = 150
        final = total + shipping

    return render(request, "cart.html", {'cart': c, 'total': total, 'shipping': shipping, 'final': final, })


def deleteCart(request, pid):
    cart = request.session.get('cart', None)
    if (cart):
        for key in cart.keys():
            if (str(pid) == key):
                del cart[key]
                break
        request.session['cart'] = cart
    return redirect("/cart")



    # views.py
from django.shortcuts import render, redirect

def updateCart(request, pid, op):
    # Your implementation here
    pass



# FOR WISHLIST PAGE

# def wishlist(request):
#     cart = request.session.get('wishlist',None)
#     if wishlist is not None:
#         print(wishlist)
#     else:
#         pass
#     return render(request,"wishlistPage.html")
