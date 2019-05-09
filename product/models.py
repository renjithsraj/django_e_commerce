from django.db import models
from django.utils import timezone

# from apps.slugu import *

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField

import mptt
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Section
class Section(MPTTModel):

    name = models.CharField(max_length=50, unique=True)

    feauterd_image = ProcessedImageField(upload_to='images/category',
                                         format='JPEG',
                                         options={'quality': 60}, null=True, blank=True, verbose_name="image(height:346px,width:895px)")
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    image_thumbnail = ImageSpecField(source='feauterd_image',
                                     processors=[ResizeToFill(233, 233)],
                                     format='JPEG',
                                     options={'quality': 60})

    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    url = models.CharField(max_length=255, null=True, blank=True)

    is_menu = models.BooleanField(default=False, verbose_name="Is Menu")

    def short_image(self):
        if self.image_thumbnail:
            return u'<img src="%s" />' % self.image_thumbnail.url

    short_image.short_description = 'Thumbnail'
    short_image.allow_tags = True

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name
        
# Product
class Products(models.Model):

    slug = models.SlugField(
        max_length=1000, unique=True, null=True, blank=True)

    name = models.CharField(max_length=500, verbose_name='Heading')
    date = models.DateField(verbose_name="Date")

    category = TreeManyToManyField(
        Section, related_name='products')

    specification = RichTextField(verbose_name='spacification for a product')

    product_no = models.IntegerField()

    Note = models.TextField(max_length=500, verbose_name='Any Notes')

    Features = RichTextField(
        verbose_name='features of products', null=True, blank=True)

    url = models.CharField(
        verbose_name='working of this Products video url ', max_length=1000, null=True, blank=True)

    content = RichTextField(verbose_name='Content')

    dummy_price = models.FloatField(null=True, blank=True)

    price = models.FloatField(default=0.0)

    weight = models.FloatField(default=0.0, verbose_name="Weight in grams")

    meta_keywords = models.TextField(
        verbose_name="Meta Keywords", null=True, blank=True)

    meta_description = models.TextField(
        verbose_name="Meta Description", null=True, blank=True)

    count = models.IntegerField()

    is_slide = models.BooleanField(
        default=False, verbose_name="Show in slider ?")

    image_slider = ImageSpecField(source='image',
                                  processors=[ResizeToFill(262, 220)],
                                  format='JPEG',
                                  options={'quality': 60})
    image = ProcessedImageField(upload_to='images/blog',
                                format='JPEG',
                                          options={'quality': 60}, verbose_name="Image (828px X 363px)")

    tax_included = models.BooleanField(default=True)

    service_tax = models.FloatField(
        default=0.0, verbose_name="Service tax(mention in  percetage)")
    sales_tax = models.FloatField(
        default=0.0, verbose_name="Sales tax(mention in  percetage)")
    vat = models.FloatField(
        default=0.0, verbose_name="Value Added Tax(mention in  percetage)")
    cess = models.FloatField(
        default=0.0, verbose_name="Cess Tax(mention in percetage)")
    cst = models.FloatField(
        default=0.0, verbose_name="Central Sales Tax(mention in  percetage)")

    is_featured = models.BooleanField(default=False)

    is_hot = models.BooleanField(default=False)

    active = models.BooleanField(default=True, verbose_name="Active or Not")

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(233, 233)],
                                     format='JPEG',
                                     options={'quality': 60})
    image_thumbnail2 = ImageSpecField(source='image',
                                      processors=[ResizeToFill(60, 60)],
                                      format='JPEG',
                                      options={'quality': 60})

    def __unicode__(self):
        return self.name

    def order_image(self):
        if self.image_thumbnail2:
            return u'<img src="%s" />' % self.image_thumbnail2.url

    def short_image(self):
        if self.image_thumbnail:
            return u'<img src="%s" />' % self.image_thumbnail.url

    short_image.short_description = 'Thumbnail'
    short_image.allow_tags = True

    def gross_pay(self):
        service_tax = self.price*self.service_tax/100
        sales_tax = self.price*self.sales_tax/100
        vat = self.price*self.vat/100
        cess = self.price*self.cess/100
        cst = self.price*self.cst/100

        if not self.tax_included:
            gross_pay = self.price + service_tax + sales_tax + vat + cess + cst
            product_actual_price = self.price
        else:
            gross_pay = self.price
            product_actual_price = self.price - \
                (service_tax + sales_tax + vat + cess + cst)

        price_list = [gross_pay, service_tax, sales_tax,
                      vat, cess, cst, product_actual_price]

        return price_list

    def sections(self):
        section = []
        for category in self.category.all():
            section.append(category)
        return section

    def image_dispaly(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/no-profile.png'

    def save(self):
        if not self.slug:
            name1 = unidecode(self.name)
            unique_slugify(self, name1)
        else:
            pass

        super(Products, self).save()

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")


# product ImageGallery
class ImageGallery(models.Model):

    product = models.ForeignKey(Products, related_name="gallery", on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100, verbose_name="Image Name", null=True, blank=True)

    image = ProcessedImageField(upload_to='images/blog',
                                format='JPEG',
                                options={'quality': 60}, verbose_name="Blog Image (828px X 363px)")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(90, 90)],
                                     format='JPEG',
                                     options={'quality': 60})

    def __unicode__(self):
        return self.product.name + " - " + self.name

    def short_image(self):
        if self.image_thumbnail:
            return u'<img src="/media/%s" />' % self.image_thumbnail

    short_image.short_description = 'Thumbnail'
    short_image.allow_tags = True


class Resources(models.Model):

    """ Resurce stores the detailed information about curresponding product """

    product = models.ForeignKey(Products, related_name="resources", on_delete= models.CASCADE)

    heading = models.CharField(max_length=500, verbose_name='Heading')
    date = models.DateField(verbose_name="Published Date")

    author = models.CharField(max_length=500, verbose_name='name')

    image = ProcessedImageField(upload_to='images/blog',
                                format='JPEG',
                                       options={'quality': 60}, verbose_name="Blog Image (828px X 363px)", null=True, blank=True)

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(350, 220)],
                                     format='JPEG',
                                     options={'quality': 60})

    discription = RichTextField(verbose_name='discription about the product')

    tutorial = models.TextField(
        verbose_name="How to use", null=True, blank=True)

    specification = models.TextField(
        verbose_name="Specification", null=True, blank=True)

    active = models.BooleanField(
        default=True, verbose_name="resource Active or Not")

    is_featured = models.BooleanField(
        default=False, verbose_name="resource featured or Not (only one)")

    def image_display(self):

        if not self.image_thumbnail:
            return '/static/images/nouser.png'
        else:
            return self.image_thumbnail.url

    def __unicode__(self):
        return self.heading

    def short_image(self):
        if self.image_thumbnail:
            return u'<img src="%s" />' % self.image_thumbnail.url

    short_image.short_description = 'Thumbnail'
    short_image.allow_tags = True

    class Meta:
        verbose_name = ("Resource")
        verbose_name_plural = ("Resources")


class ResourceGallery(models.Model):

    resources = models.ForeignKey(Resources, related_name="rgallery", on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100, verbose_name="Image Name", null=True, blank=True)
    image = ProcessedImageField(upload_to='images/blog',
                                format='JPEG', options={'quality': 60}, verbose_name="Blog Image (828px X 363px)")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(90, 90)],
                                     format='JPEG',
                                     options={'quality': 60})

    def __unicode__(self):
        return self.resources.heading + " - " + self.name

    def image_display(self):

        if not self.image_thumbnail:
            return '/static/images/nouser.png'
        else:
            return self.image_thumbnail.url

    def short_image(self):
        if self.image_thumbnail:
            return u'<img src="/media/%s" />' % self.image_thumbnail

    short_image.short_description = 'Thumbnail'
    short_image.allow_tags = True


mptt.register(Section)
