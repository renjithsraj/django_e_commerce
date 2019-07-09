from django import template
register = template.Library()
from product.models import Section

# Category listing tags for side nav bs
@register.inclusion_tag('tags/category_side.html', takes_context=True)
def side_category_tag(context, user=None):
    categories = Section.objects.filter(parent__isnull=True)
    return {'nodes': categories}

@register.inclusion_tag('tags/category_side_1.html', takes_context=True)
def side_category_tag_1(context, user=None):
    categories = Section.objects.filter(parent__isnull=True)
    return {'nodes': categories}


@register.inclusion_tag('tags/tree_structure.html', takes_context=True)
def tree_structure(context, category):
    subs = category.children.all()
    return {"subs": subs}
