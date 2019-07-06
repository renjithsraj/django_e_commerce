from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View, generic
from product.models import Products
from buyer.models import WishList
from product.utils import JSONResponseMixin
from product.serializers import ProductsSerializer
from django.shortcuts import get_object_or_404

import  json

# Project detail view ajax and normal request
class ProductDetailView(JSONResponseMixin, DetailView):
    model = Products
    template_name = 'product/products_detail.html'

    def render_to_response(self, context):
        if self.request.is_ajax():
            product_json = ProductsSerializer(
                context['object'], context={"request": self.request}).data
            return self.render_to_json_response(product_json)
        else:
            return super().render_to_response(context)

# Save Product item into wishlist and get the total wish list based on 
# the Authenticated User


class WishlistView(JSONResponseMixin, generic.ListView):
    # template_name = 'form_template.html'
    model = WishList

    def get(self, request, *args, **kwargs):
        # return render(request, self.template_name, {'form': form})
        pass
    
    def get_queryset(self, slug=None):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, 
            product= get_object_or_404(Products, slug=slug))
    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            rq = request.POST.get
            if not rq('product_slug'):
                return self.render_to_json_response(
                    {
                        "status": "error",
                        "msg": "Project ID does'nt exists"
                    }
                )
            if not self.get_queryset(slug=rq('product_slug')).exists():
                self.model.objects.create(
                    user=request.user,
                    product=get_object_or_404(
                        Products, slug=rq('product_slug')),
                    email=request.user.id
                )
                return self.render_to_json_response(
                    {
                        "status": "success",
                        "msg": "successfully added item into wish list"
                    }
                )
            else:
                return self.render_to_json_response(
                    {
                        "status": "error",
                        "msg": "Product Item already in Wishlist"
                    }
                )


    

