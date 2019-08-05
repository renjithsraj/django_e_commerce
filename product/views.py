from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views import View, generic
from product.utils import JSONResponseMixin
from product.serializers import ProductsSerializer
from django.shortcuts import get_object_or_404
import  json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Apps Models 
from product.models import Products, Section
from billing.models import Cart, CartItem
from buyer.models import Buyer, WishList
from billing.views import tax_fu, grand_total_fu

def move_to_cart(request):
    buyer = Buyer.objects.get(id=request.user.id)
    if 'cart' in request.session:
        cart_list = request.session['cart']
        try:
            cart_obj = get_object_or_404(Cart, buyer=buyer)
        except :
            cart_obj = Cart(buyer=buyer).save()
        for item in cart_list:
            product = get_object_or_404(Products, id=int(item['id']))
            if CartItem.objects.filter(buyer=buyer, product=product).exists():
                cart_item = CartItem.objects.get(buyer=buyer, product=product)
                q = cart_item.quantity + int(item['qty'])
                cart_item.delete()
                cart_item = CartItem(buyer=buyer, 
                        product=product, quantity=q)
                cart_item.save()
            else:
                cart_item = CartItem(buyer=buyer, 
                        product=product, quantity=int(item['qty'])
                    )
                cart_item.save()
            cart_obj.items.add(cart_item)
        cart_obj.save()
    else:
        pass



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
    template_name = 'product/wishlist.html'
    model = WishList
    # login_url = '/account-login/'
    redirect_field_name = '/wish-list'
    context_object_name = 'wishlists'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'GET'] and not request.user.is_authenticated:
            return self.render_to_json_response({
                "status": "login_error",
                "msg": "Please login to access Wish list"
            })
        return super(WishlistView, self).dispatch(request, *args, **kwargs)

    def redirect_url(self):
        return redirect("/accounts/login /?next=/wish-list/")

    def get(self, request, *args, **kwargs):
        user_wishlist_data = self.model.objects.filter(user__id= request.user.id
                ).order_by('-added_on')
        if request.is_ajax():
            return self.render_to_json_response({
                'status': 'success',
                'wish_list_count': user_wishlist_data.count()})
        return render(request, self.template_name, {'wishlist': ''})

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
    resp = {"status": "", "msg": "", "count": 0}

    def get(self, request, *args, **kwargs):
        # request.session.clear()
        price, count = 0, 0
        product_carts= []
        html_string = ""
        if request.user.is_authenticated:
            cart_list = CartItem.objects.filter(buyer__id = request.user.id)
            for cart_item in cart_list:
                price += cart_item.total
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
                    """.format(cart_item.product.name, cart_item.product.image_thumbnail.url, 
                    cart_item.quantity, format(cart_item.product.gross_pay()[0], '.2f'), 
                    format(cart_item.total, '.2f'), cart_item.product.product_no)
                product_carts.append(cart_data)
                total_html = """
                                <li>
                                    <span><span>Sub Total</span></span><span>${0}</span>
                                </li>
                                <li>
                                    <ul class="checkout">
                                        <li><a href="/checkout" class="btn-checkout"><i class="fa fa-shopping-cart" aria-hidden="true"></i>View Cart</a></li>
                                        <li><a href="/checkout" class="btn-checkout"><i class="fa fa-share" aria-hidden="true"></i>Checkout</a></li>
                                    </ul>
                                </li>""".format(price)
                html_string = "".join(product_carts) + total_html
            self.resp.update({
                'status': "success", 'data': html_string,
                'msg': "successfuly loaded", 
                "count": len(product_carts) if len(product_carts) > 0 else 0, 
                "total": price})

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
                                        <li><a href="checkout" class="btn-checkout"><i class="fa fa-shopping-cart" aria-hidden="true"></i>View Cart</a></li>
                                        <li><a href="/checkout" class="btn-checkout"><i class="fa fa-share" aria-hidden="true"></i>Checkout</a></li>
                                    </ul>
                                </li>""".format(price)
                html_string = "".join(product_carts) + total_html   
            self.resp.update({
                'status': "success", 'data': html_string, 
                'msg': "successfuly loaded", 
                "count": len(product_carts) if len(product_carts) > 0 else 0, 
                "total": price})
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


class ProductCategoryListView(JSONResponseMixin ,View):
    model = Section
    template_name = "product/product_category.html"

    def get(self, request, *args, **kwargs):
        section = get_object_or_404(self.model, slug=kwargs.get('slug'))
        child_categories = [ cat.id for cat in section.get_descendants()]
        child_categories.append(section.id)
        products = Products.objects.filter(
            category__id__in=child_categories).order_by('-date').distinct()
        paginator = Paginator(products, 10) 
        page = self.request.GET.get('page')
        try:
            products_list = paginator.page(page)
        except PageNotAnInteger:
            products_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            products_list = paginator.page(paginator.num_pages)
        print(products)
        return render(request, self.template_name, {'page': page, "products_list": products_list})
    
@login_required
def checkout(request):
    items, srate, tax, grand_total  = None, 0.0, 0.0, 0.0
    cart_items = CartItem.objects.filter(buyer__id=request.user.id)
    if not cart_items:
        extra = "Cart empty"
        return render(request, 
            'product/checkout.html', 
            {'extra': extra}
        )
    try:
        cart = Cart.objects.get(buyer=request.user)
    except ObjectDoesNotExist:
        extra = "You dont have any item in your cart"
        return render(request, 
            'product/checkout.html', 
            {'extra': extra}
        )
    tax = tax_fu(cart)
    srate, grand_total, items = grand_total_fu(cart_items)
    data = { 'items': items, 'srate': srate, 
            'tax': tax, 'grand_total': grand_total}
    return render(
        request, 'product/checkout.html', data
    )