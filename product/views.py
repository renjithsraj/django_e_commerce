from django.shortcuts import render
from django.views.generic.detail import DetailView
from product.models import Products
from product.utils import JSONResponseMixin
from product.serializers import ProductsSerializer
import  json

class ProductDetailView(JSONResponseMixin, DetailView):
    model = Products
    template_name = 'product/products_detail.html'

    def render_to_response(self, context):
        if self.request.is_ajax():
            product_json = ProductsSerializer(context['object']).data
            return self.render_to_json_response(product_json)
        else:
            return super().render_to_response(context)

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     print ("the data is", self.object.price)



    

