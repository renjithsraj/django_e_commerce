from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# from passlib.hash import pbkdf2_sha512

import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

import hashlib
from django.shortcuts import redirect


from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Min, Sum, Avg


from django.conf import settings
from product.models import *
from buyer.models import *
from shipping.models import *
from billing.models import *





"""----------------------Helping functions---------------------"""


def grand_total_fu(cart):
    """ Function use for calculating total weight and price and items in cart
     for checkout.html"""
    items = cart.all()
    total = 0.0
    grand_total = 0.0
    srate = 0.0
    total_weight = []
    for p in items:
        total_w = p.quantity * p.product.weight
        total_weight.append(total_w)
    total += sum(total_weight)
    try:
        srate = ShippingRate.objects.get(value1__lt=total, value2__gte=total)
        srate = srate.price

    except:
        srate = settings.DEFAULT_SHIPPING_RATE
    if srate:
        # print srate
        price = 0.0
        grand_total = 0.0

        for item in cart:
            price += item.total
            grand_total = srate + price
    yield srate
    yield grand_total
    yield items


def tax_fu(cart):
    """ return the different taxes of  Products after adding to cart"""
    tax_list = [0.0, 0.0, 0.0, 0.0, 0.0, ]
    if cart:
        for order in cart.items.all():

            tax_list[0] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.service_tax / 100)

            tax_list[1] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.sales_tax / 100)

            tax_list[2] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.vat / 100)

            tax_list[3] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.cess / 100)

            tax_list[4] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.cst / 100)
        tax_list[0]
    return tax_list


def myorder_tax_fu(cart):
    """ return the different taxes of  Products after adding to cart"""
    tax_list = [0.0, 0.0, 0.0, 0.0, 0.0, ]
    if cart:
        for order in cart.items.all():
            tax_list[0] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.service_tax / 100)

            tax_list[1] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.sales_tax / 100)

            tax_list[2] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.vat / 100)

            tax_list[3] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.cess / 100)

            tax_list[4] += (order.product.gross_pay()[0] * order.quantity) * \
                (order.product.cst / 100)
        tax_list[0]
    return tax_list


# functions for calculating grand total
def total_price_fu(order):
    """ funtions for calculating total price """

    total_details = {}
    items = order.items.all()
    total_price = 0.0
    shipping_rate = 0.0
    total_weight = 0.0

    for order_item in items:
        total_price += order_item.total_amount
        total_weight += order_item.weight * order_item.quantity

    try:
        shipping_rate = ShippingRate.objects.get(
            value1__lt=total_weight, value2__gte=total_weight)
        total_details['shipping_rate'] = shipping_rate.price

    except:
        shipping_rate = float(settings.DEFAULT_SHIPPING_RATE)
        total_details['shipping_rate'] = shipping_rate

    total_details['total_price'] = total_price

    total_details['grand_total'] = float(
        total_price) + float(total_details['shipping_rate'])
    return total_details







