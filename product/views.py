from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View
from product.models import Products
from product.utils import JSONResponseMixin
from product.serializers import ProductsSerializer
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

class WishlistView(View):
    # template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        # return render(request, self.template_name, {'form': form})
        pass

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            pass


    

