from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings
from decimal import Decimal
from ecomapp.models import *
from django.http import HttpResponseRedirect,JsonResponse
from ecomapp.forms import *
from django.views.generic import TemplateView
from django.template import RequestContext
# Create your views here.

def base_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart_id = request.session.get('cart_id')

    if cart_id is None:#мына кодты тек осы жерде тұр
        cart = Cart.objects.create()
        cart_id = cart.id
        request.session['cart_id'] = cart.id

    categories=Category.objects.all()
    products=Product.objects.filter(available=True)

    context={
        'categories':categories,
        'products':products,
        'cart':cart
    }
    return render(request,'base.html',context)


def product_view(request, product_slug):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id


    product=Product.objects.get(slug=product_slug)
    categories=Category.objects.all()

    context={
        'categories':categories,
        'product':product,
        'cart':cart
    }
    return render(request,'product.html',context)


def category_view(request, category_slug):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    category=Category.objects.get(slug=category_slug)
    categories=Category.objects.all()
    products_of_category=Product.objects.filter(category=category)

    context={
        'category':category,
        'products_of_category':products_of_category,
        'categories':categories,
        'cart':cart
    }
    return render(request,'category.html',context)

def cart_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    context={
        'cart':cart,
    }
    return render(request,'cart.html', context)


def add_to_cart_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    product_slug=request.GET.get('product_slug')
    product=Product.objects.get(slug=product_slug)

    cart.add_to_cart(product_slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total+=float(item.item_total)
    cart.cart_total=new_cart_total
    cart.save()

    return JsonResponse({'cart_total':cart.items.count(),'cart_total_price':cart.cart_total})



def remove_from_cart_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    product_slug=request.GET.get('product_slug')
    product=Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)

    new_cart_total= 0.00
    for item in cart.items.all():
        new_cart_total+=float(item.item_total)
    cart.cart_total=new_cart_total
    cart.save()

    return JsonResponse({'cart_total':cart.items.count(),'cart_total_price':cart.cart_total})


def change_item_qty(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    qty=request.GET.get('qty')
    item_id=request.GET.get('item_id')
    #cart_item=CartItem.objects.get(id=int(item_id))
    cart.change_qty(qty, item_id)
    cart_item=CartItem.objects.get(id=int(item_id))
    return JsonResponse(
    {'cart_total':cart.items.count(),
    'item_total':cart_item.item_total,
    'cart_total_price':cart.cart_total
    })


def checkout_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    context={
        'cart':cart
    }
    return render(request,'checkout.html',context)


def order_create_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    form=OrderForm(request.POST or None)
    context={
        'form':form,
        'cart':cart
    }
    return render(request,'order.html',context)




def make_order_view(request):
    carts = Cart.objects.filter(pk=request.session.get('cart_id'))
# I'm not fully sure None is accepted here, use -1 if it's not.

    if carts:
        cart = carts[0]
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order()
        new_order.user=request.user
        new_order.save()
        new_order.items.add(cart)
        new_order.first_name=name
        new_order.last_name=last_name
        new_order.phone=phone
        new_order.address=address
        new_order.buying_type=buying_type
        new_order.comments=comments
        new_order.total=cart.cart_total
        new_order.save()
        del request.session['cart_id']
        #del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
