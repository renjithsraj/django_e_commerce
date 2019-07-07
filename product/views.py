from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View, generic
from product.utils import JSONResponseMixin
from product.serializers import ProductsSerializer
from django.shortcuts import get_object_or_404
import  json

# Apps Models 
from product.models import Products
from billing.models import Cart, CartItem
from buyer.models import Buyer, WishList



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

# Add Product into cart for authenticated User and anonymous User
class AddProductCartView(JSONResponseMixin, generic.ListView):
    # template_name = 'form_template.html'
    model = Products
    cart_required_params = [
        'product_slug', 'csrfmiddlewaretoken', 'qty', 'quick']
    resp = {"status": "", "msg": ""}

    def get(self, request, *args, **kwargs):
        # request.session['cart'] = []
        print(request.session.get('cart', []))

    def post(self, request, *args, **kwargs):
        rq = request.POST.get
        for require_item in self.cart_required_params:
            if not rq(require_item):
                return self.render_to_json_response(
                    {
                        "status": "error",
                        "msg": "Missing {0} in Requests".format(require_item)
                    }
                )
        product = get_object_or_404(Products, slug=rq('product_slug'))
        if request.user.is_authenticated:
            buyer = Buyer.objects.get(id=request.user.id)
            try:
                cart_obj = Cart.objects.get(buyer = buyer)
            except Cart.DoesNotExist:
                cart_obj = Cart.objects.create(buyer = buyer)
            if CartItem.objects.filter(buyer=buyer, product=product).exists():
                cart_item = CartItem.objects.get(buyer=buyer, product=product)
                if product.count >= (cart_item.quantity + int(rq('qty'))):
                    q = cart_item.quantity + int(rq('qty'))
                    cart_item.delete()
                    cart_item = CartItem(
                        buyer=buyer, product=product, quantity=q)
                    cart_item.save()
                    cart_obj.items.add(cart_item)
                    cart_obj.save()
                    self.resp.update({
                        'status': 'success',
                        'msg': "Successfully added new prodct : {0}".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
                else:
                    self.resp.update({
                        'status': 'error',
                        'msg': "We don't have enough {0} stock on hand for the quantity you selected. Please try again".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
            else:
                if product.count >= int(rq('qty')):
                    cart_item = CartItem(
                        buyer=buyer, product=product, quantity=int(rq('qty')))
                    cart_item.save()
                    cart_obj.items.add(cart_item)
                    cart_obj.save()
                    self.resp.update({
                        'status': 'success',
                        'msg': "Successfully added new prodct : {0}".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
                else:
                    self.resp.update({
                        'status': 'error',
                        'msg': "We don't have enough {0} stock on hand for the quantity you selected. Please try again".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
        else:
            cart_list, added = [], False
            if 'cart' in request.session:
                cart_list = request.session['cart']
            selected_item = {}
            for item in cart_list:
                if item['id'] == product.id:
                    selected_item = item
                    added = True
            if added:
                qty = selected_item['qty']
                if product.count >= (int(qty) + int(rq('qty'))):

                    qty = int(qty) + int(rq('qty'))
                    cart_list.remove(selected_item)
                    total = float(product.gross_pay()[0]) * int(qty)
                    cart_list.append({'id': product.id, 'name': product.name, 'slug': product.slug, 
                            'image':product.image.url, 'qty': qty, 
                            'price': product.gross_pay()[0], 'total': total, }
                            )
                else:
                    self.resp.update({
                        'status': 'error', 
                        'msg': "We don't have enough {0} stock on hand for the quantity you selected. Please try again".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
            else:
                if int(product.count) >= int(rq('qty')):
                    total = float(product.gross_pay()[0]) * int(rq('qty'))
                    cart_list.append({'id': product.id, 'name': product.name, 
                    'slug': product.slug, 'image': product.image.url, 
                    'qty': rq('qty'), 'price': product.gross_pay()[0], 
                    'total': total 
                    })
                else:
                    self.resp.update({
                        'status': 'error',
                        'msg': "We don't have enough {0} stock on hand for the quantity you selected. Please try again".format(str(product.name))})
                    return self.render_to_json_response(self.resp)
            request.session['cart'] = cart_list
            self.resp.update({
                'status': 'success',
                'msg': "Successfully added {0} into cart".format(str(product.name))})
            return self.render_to_json_response(self.resp)


