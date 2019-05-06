from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import random
import re
from django.conf import settings
from datetime import timedelta

from product.models import Products
from shipping.models import Country

class Pincode(models.Model):

    pincode = models.CharField(
        max_length=100, verbose_name=u'available pincode', null=True, blank=True)

    def __unicode__(self):
        return self.pincode


# Buyer Manager

class BuyerManager(models.Manager):

    def verify_user(self, verification_code):
        if re.match('[a-f0-9]{40}', verification_code):
            try:
                buyer = self.get(verification_code=verification_code)
            except self.model.DoesNotExist:
                return False
            if not buyer.verification_code_expired():
                # Account exists and has a non-expired key. Activate it.
                buyer.is_verifed = True
                buyer.save()
                return True
            return False

# Buyer Details


class Buyer(User):
    street_address = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(
        verbose_name=u'Country', max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)

    verification_code = models.CharField(max_length=200, null=True, blank=True)
    is_verifed = models.BooleanField(default=False)
    key_generated = models.DateTimeField(null=True, blank=True)

    objects = BuyerManager()

    def __unicode__(self):
        return self.first_name

    class Meta:
        verbose_name = ("Buyer")
        verbose_name_plural = ("Buyers")

    def verification_code_expired(self):
        expiration_date = datetime.timedelta(
            days=settings.VERIFICATION_EXPIRY_DAYS)
        return self.key_generated + expiration_date <= timezone.now()

    def verify_user(self, verification_key):
        EndDate = self.key_generated + \
            timedelta(days=settings.VERIFICATION_EXPIRY_DAYS)
        if re.match('[a-f0-9]{40}', verification_key) and EndDate >= datetime.now().date():
            try:
                self.save()
                return True
            except:
                return False


class WishList(models.Model):
    product = models.ForeignKey(Products, related_name='wishlist', on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    added_on = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
