from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import Coffee, Cart,Order
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
import razorpay

# Create your views here.
def main(req):
    return render(req,"main.html")

def index(req):
    username = req.user.username
    allproducts = Coffee.objects.all()
    context = {"allproducts": allproducts, "username": username}
    return render(req, "index.html", context)


def register(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "register.html", context)
        elif ucpass != upass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "register.html", context)
        else:
            try:
                u = User.objects.create(username=uname, password=upass)
                u.set_password(upass)
                u.save()
                return redirect("/userlogin")
            except Exception:
                context["errmsg"] = "User already exists"
                return render(req, "register.html", context)
    else:
        return render(req, "register.html")


def userlogin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" and upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "login.html", context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(req, u)
                return redirect("/index")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "login.html", context)
    else:
        return render(req, "login.html")


def userlogout(req):
    logout(req)
    return redirect("/")


def add_to_cart(request, coffee_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    allproducts = get_object_or_404(Coffee, coffee_id = coffee_id)
    cart_item, created = Cart.objects.get_or_create(coffee_id = allproducts, userid=user)
    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1
    cart_item.save()

    return redirect("/cart")


def cart(req):
    if req.user.is_authenticated:
        username = req.user.username
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.coffee_id.price * x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
            "username": username,
        }
        return render(req, "cart.html", context)
    else:
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.coffee_id.price * x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
        }
        return render(req, "cart.html", context)

def placeorder(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=None
    # user=request.user.id
    allcarts = Cart.objects.filter(userid=user)
    order_id=random.randrange(1000,9999)
    for x in allcarts:
        o=Order.objects.create(order_id=order_id,coffee_id=x.coffee_id,userid=x.userid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(userid=user)
    total_price = 0
    length = len(orders)
    for x in orders:
        total_price += x.coffee_id.price * x.qty
    context={}
    context['cart_items']=orders
    context['total']=total_price
    context['items']=length
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(userid=request.user)
    total_price = 0
    for x in orders:
        total_price += x.coffee_id.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_UlbO35bHqiCAbm", "nceh3T6nR5SEq6TfacTEM7gt"))
    data = { "amount": total_price*100, "currency": "INR", "receipt": str(oid) }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['data']=payment
    # context['amount']=payment
    return render(request,'payment.html',context)

def remove_from_cart(request, coffee_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_item = Cart.objects.filter(coffee_id=coffee_id, userid=user)
    cart_item.delete()
    return redirect("/cart")

def remove_from_order(request, coffee_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    orders=Order.objects.filter(userid=user,coffee_id=coffee_id)
    orders.delete()
    return redirect("/cart")



def coffeelistview(request):
    if request.method == "GET":
        allproducts = Coffee.prod.Coffee_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Coffee.objects.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)


def dessertlistview(request):
    if request.method == "GET":
        allproducts =Coffee.prod.Dessert_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Coffee.objects.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)


def sanckslistview(request):
    if request.method == "GET":
        allproducts = Coffee.prod.Sancks_list()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)
    else:
        allproducts = Coffee.object.all()
        context = {"allproducts": allproducts}
        return render(request, "index.html", context)





def searchproduct(request):
    query = request.GET.get("q")
    if query:
        allproducts = Coffee.objects.filter(
            Q(coffee_name__icontains=query)
            | Q(category__icontains=query)
            | Q(price__icontains=query)
        )
    else:
        allproducts = Coffee.objects.all()
    context = {"allproducts": allproducts, "query": query}
    return render(request, "index.html", context)


def updateqty(request, qv, coffee_id):
    allcarts = Cart.objects.filter(coffee_id=coffee_id)
    if qv == "1":
        totol = allcarts[0].qty + 1
        allcarts.update(qty=totol)
    else:
        if allcarts[0].qty > 1:
            totol = allcarts[0].qty - 1
            allcarts.update(qty=totol)
        else:
            allcarts = Cart.objects.filter(coffee_id=coffee_id)
            allcarts.delete()

    return redirect("/cart")
