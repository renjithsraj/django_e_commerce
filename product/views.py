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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_products"] = self.model.objects.filter(category__in=
            [i.id for i in self.object.category.all()]).exclude(slug= self.object.slug)
        return context
    

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
        # request.session.clear()
        price, count = 0, 0
        product_carts= [] = ""
        html_string = ""
        if request.user.is_authenticated:
            pass
        else:
            if 'cart' in request.session:
                cart_list = request.session.get('cart')
                product_carts = []
                for cart_item in cart_list:
                    price += cart_item['total']
                    cart_data = """ 
                            <li>
                                <div class="cart-single-product">
                                    <div class="media">
                                        <div class="pull-left cart-product-img">
                                            <a href="index.html#">
                                                <img class="img-responsive" alt="{0}" src="{1}">
                                            </a>
                                        </div>
                                        <div class="media-body cart-content">
                                            <ul>
                                                <li>
                                                    <h2><a href="index.html#">{0}</a></h2>
                                                    <h3><span>Code:</span> {5}</h3>
                                                </li>
                                                <li>
                                                    <p>X {2}</p>
                                                </li>
                                                <li>
                                                    <p>${3}</p>
                                                </li>
                                                <li>
                                                    <p>${4}</p>
                                                </li>
                                                <li> <a class="trash" onclick=""><i class="fa fa-trash-o"></i></a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </li>
                    """.format(cart_item['name'], cart_item['image'],cart_item['qty'], cart_item['price'], cart_item['total'], cart_item['code'])
                    product_carts.append(cart_data)
                total_html = """
                                <li>
                                    <span><span>Sub Total</span></span><span>${0}</span>
                                </li>
                                <li>
                                    <ul class="checkout">
                                        <li><a href="cart.html" class="btn-checkout"><i class="fa fa-shopping-cart" aria-hidden="true"></i>View Cart</a></li>
                                        <li><a href="check-out.html" class="btn-checkout"><i class="fa fa-share" aria-hidden="true"></i>Checkout</a></li>
                                    </ul>
                                </li>""".format(price)
                html_string = "".join(product_carts) + total_html   
            self.resp.update({
                'status': "success", 'data': html_string, 
                'msg': "successfuly loaded", "count": len(product_carts), "total": price})
        return self.render_to_json_response(self.resp)


        


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
                            'price': product.gross_pay()[0], 'total': total, 
                            'code': product.product_no}
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
                    'total': total, 'code': product.product_no
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


