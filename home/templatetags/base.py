from django import template
register = template.Library()
from product.models import Section, Products
from django.shortcuts import get_object_or_404

# Category listing tags for side nav bs
@register.inclusion_tag('tags/category_side.html', takes_context=True)
def side_category_tag(context, user=None):
    categories = Section.objects.filter(parent__isnull=True)
    return {'nodes': categories}

# Category listing tags for side nav bs
@register.inclusion_tag('tags/menu_ul_tag.html', takes_context=True)
def menu_category_tag(context, user=None):
    categories = Section.objects.filter(parent__isnull=True)
    return {'nodes': categories}

@register.inclusion_tag('tags/category_side_1.html', takes_context=True)
def side_category_tag_1(context, product_id=None,  user=None):
    product = get_object_or_404(Products, id=product_id)
    category_ids = [ i.id for i in product.category.all()]
    related_products = Products.objects.filter(category__in = category_ids
    ).exclude(id=product_id)
    categories = Section.objects.filter(parent__isnull=True)
    return {'nodes': categories, 'related_products': related_products, 'product': product}


@register.inclusion_tag('tags/tree_structure.html', takes_context=True)
def tree_structure(context, category):
    subs = category.children.all()
    return {"subs": subs}

def get_categories():
    categories = Section.objects.filter(
        parent__isnull=True, is_menu=True).order_by('-id')
    return categories

@register.inclusion_tag('tags/main_header.html', takes_context=True)
def main_header(context, user=None):
    categories = get_categories()
    return {'nodes': categories}
