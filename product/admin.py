from django.contrib import admin
from .models import Section, Products, ImageGallery, Resources, ResourceGallery

from mptt.admin import MPTTModelAdmin


class SectionAdmin(MPTTModelAdmin):
    model = Section


class ImageGalleryAdmin(admin.ModelAdmin):
    model = ImageGallery
    list_display = ('product', 'short_image',)


class ImageGalleryInline(admin.StackedInline):
    model = ImageGallery
    list_display = ('name', 'short_image',)

    extra = 3


class ProductsAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('name', 'short_image',)

    inlines = (ImageGalleryInline,)


class ResourceGalleryAdmin(admin.ModelAdmin):
    model = ResourceGallery
    list_display = ('resources', 'short_image',)


class ResourceGalleryInline(admin.StackedInline):
    model = ResourceGallery
    list_display = ('name', 'short_image',)
    extra = 3


class ResourceAdmin(admin.ModelAdmin):
    model = Resources
    list_display = ('heading', 'short_image',)
    inlines = (ResourceGalleryInline,)


admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(ResourceGallery, ResourceGalleryAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Resources, ResourceAdmin)
