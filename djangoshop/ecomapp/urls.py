from django.conf.urls import url
from ecomapp.views import *
from django.views.generic import TemplateView

#app_name = 'ecomapp'

urlpatterns = [
    url(r'^$',base_view,name='base'),
    url(r'^category/(?P<category_slug>[-\w]+)/$',category_view,name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$',product_view,name='product_detail'),
    url(r'^cart/$',cart_view,name='cart'),
    url(r'^add_to_cart/$',add_to_cart_view,name='add_to_cart'),
    url(r'^remove_from_cart/$',remove_from_cart_view,name='remove_from_cart'),
    url(r'^change_item_qty/$',change_item_qty,name='change_item_qty'),
    url(r'^checkout/$',checkout_view,name='checkout'),
    url(r'^order/$',order_create_view,name='create_order'),
    url(r'^make_order/$', make_order_view, name='make_order'),
    #url(r'^order/$',order_create_view,name='create_order'),
    url(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
]
