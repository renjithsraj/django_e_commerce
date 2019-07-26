from django.db import models
from uuid import uuid4, UUID
import uuid
from ckeditor.fields import RichTextField
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from shipping.models import Country
from product.models import Products
from buyer.models import Buyer

TAX_TYPES = (('Se', 'Service Tax'), ('Sa', 'Sales Tax'),
             ('V', 'Vat'), ('C', 'Cess'))

PAYMENT_TYPE = (('OFF', 'Ofline'), ('ON', 'Online'))


class GatewayCommission(models.Model):
    name = models.CharField(verbose_name=u'Name', max_length=50)
    percentage = models.FloatField(verbose_name='Percentage')

    def __str__(self):
        return self.name


class Tax(models.Model):

    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    tax_type = models.CharField(choices=TAX_TYPES, default='Sa', max_length=2)
    percentage = models.FloatField(default=0.0)
    year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_tax_type_display()


class ShippingAddress(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    street_address = models.TextField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=50)
    state = models.CharField(null=True, blank=True, max_length=50)
    pincode = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey(
        Country, null=True, blank=True, related_name='cart', on_delete=models.CASCADE)
    mobile = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.buyer.first_name


class ShippAddress(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    street_address = models.TextField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=50)
    state = models.CharField(null=True, blank=True, max_length=50)
    pincode = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True, )
    mobile = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.buyer.first_name


class CartItem(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_on = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    total = models.FloatField(default=0.0)

    def save(self):
        self.total = self.quantity * self.product.gross_pay()[0]
        super(CartItem, self).save()

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    added_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.buyer.first_name


class OrderItem(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, null=True, blank=True)
    product_title = models.CharField(max_length=500, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    added_on = models.DateField(auto_now=True)
    weight = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.buyer.first_name + " - " + self.product_title

    def product_image(self):
        product = Products.objects.get(id=self.product_id)
        return product.image_dispaly()

    def product_slug(self):
        product = Products.objects.get(id=self.product_id)
        return product.slug


class MyOrder(models.Model):

    items = models.ManyToManyField(OrderItem)
    order_date = models.DateField(auto_now=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    txnid = models.CharField(max_length=36, primary_key=True)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    hash = models.CharField(max_length=500, null=True, blank=True)
    billing_name = models.CharField(max_length=500, null=True, blank=True)
    billing_street_address = models.CharField(
        max_length=500, null=True, blank=True)
    billing_country = models.CharField(max_length=500, null=True, blank=True)
    billing_state = models.CharField(max_length=500, null=True, blank=True)
    billing_city = models.CharField(max_length=500, null=True, blank=True)
    billing_pincode = models.CharField(max_length=500, null=True, blank=True)
    billing_mobile = models.CharField(max_length=500, null=True, blank=True)
    billing_email = models.CharField(max_length=500, null=True, blank=True)

    shipping_name = models.CharField(max_length=500, null=True, blank=True)
    shipping_street_address = models.CharField(
        max_length=500, null=True, blank=True)
    shipping_country = models.CharField(max_length=500, null=True, blank=True)
    shipping_state = models.CharField(max_length=500, null=True, blank=True)
    shipping_city = models.CharField(max_length=500, null=True, blank=True)
    shipping_pincode = models.CharField(max_length=500, null=True, blank=True)
    shipping_mobile = models.CharField(max_length=500, null=True, blank=True)
    shipping_rate = models.FloatField(null=False, blank=False, default=0.0)
    status = models.CharField(max_length=500, null=True, blank=True)
    shipping_email = models.CharField(max_length=500, null=True, blank=True)

    payment_method = models.CharField(
        max_length=1000, choices=PAYMENT_TYPE, default='ON', verbose_name='Payment-method')
    comment = models.TextField(
        null=True, blank=True, verbose_name='Comment For Product')
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)

    def total_amount(self):
        c = self.invoice_set.latest('id')
        return round(c.total_amount)

    def is_paid(self):
        i = self.invoice_set.filter(is_paid=True)
        if i.count() > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.buyer.first_name + ':' + self.txnid

class Invoice(models.Model):
    order = models.ForeignKey(MyOrder, on_delete=models.CASCADE)
    real_amount = models.FloatField(null=True, blank=True)
    discount = models.FloatField(default=0.0, null=True, blank=True)
    total_amount = models.FloatField(default=0, null=True, blank=True)
    paid_amount = models.FloatField(default=0, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    tax = models.CharField(max_length=500, null=True, blank=True)
    shipping_cost = models.FloatField(default=0.0, null=True, blank=True)
    tax_included = models.BooleanField(default=False)

    def __str__(self):
        return self.order.txnid + " - " + self.order.buyer.first_name


class Dispatched(models.Model):
    order = models.ForeignKey(MyOrder, on_delete=models.CASCADE)
    dispatched_date = models.DateField(verbose_name="Date Of Dispatched")
    message = RichTextField(verbose_name="Dispatch Message",
                            default='We are pleased to inform you that the following items in your order (____________) have been shipped.your tracking id is (_____________)')
    is_mail_send = models.BooleanField(
        default=False, verbose_name="Is Mail Send ")

    def save(self):

        if self.is_mail_send:
            order = MyOrder.objects.get(txnid=self.order.txnid)
            dispatch_mail = order.billing_email
            dispactch_date = self.dispatched_date
            dispactch_message = self.message
            subject = "your order (order id : " + \
                str(self.order.txnid)+" )has been shipped "

            val = {

                'site_url': settings.SITE_URL,
                'logo': settings.COMPANY_LOGO,
                'subject': subject,
                'message': dispactch_message,
                'date': dispactch_date,
                'order': order,
                'items': order.items.all(),

            }
            html_content = render_to_string('mail/dispatched.html', val)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to=[
                                         str(dispatch_mail), settings.DEFAULT_TO_EMAIL])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        else:
            pass

        super(Dispatched, self).save()

    def __str__(self):
        return str(self.id)
