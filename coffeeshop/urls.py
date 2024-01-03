"""
URL configuration for coffeeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from coffeeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.main,name="main"),
    path("index/", views.index, name="index"),
    path("userlogin/", views.userlogin, name="userlogin"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("register/", views.register, name="register"),
    path("cart/", views.cart, name="cart"),
    path("sanckslistview/", views.sanckslistview, name="sanckslistview"),
    path("dessertlistview/", views.dessertlistview, name="dessertlistview"),
    path("coffeelistview/", views.coffeelistview, name="coffeelistview"),
    path("searchproduct/", views.searchproduct, name="searchproduct"),

    path(
        "remove_from_cart/<int:coffee_id>",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "remove_from_order/<int:coffee_id>",
        views.remove_from_order,
        name="remove_from_order",
    ),
    path("add_to_cart/<int:coffee_id>", views.add_to_cart, name="add_to_cart"),
    path("updateqty/<qv>/<coffee_id>", views.updateqty, name="updateqty"),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('makepayment/',views.makepayment,name='makepayment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

