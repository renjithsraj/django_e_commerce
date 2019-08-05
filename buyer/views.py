from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views import View, generic
from product.utils import JSONResponseMixin
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
# Apps Models
from product.models import Products
from billing.models import Cart, CartItem
from buyer.models import Buyer, WishList
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from product.views import move_to_cart



class AccountView(View):
    template_name = 'account/user_account.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'data': ''})


class AccountLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        redirect_url = '/'
        if request.META.get('QUERY_STRING'):
            redirect_url = request.META.get('QUERY_STRING').split('next=')[1]
        return render(request, self.template_name, {'redirect_url': redirect_url})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        _url = request.POST.get('redirect_url')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            move_to_cart(request)
            return redirect(_url)
        else:
            return render(request, self.template_name, 
                {'form': form, 'redirect_url': _url}
            )
        

        
    


























# import json
# import datetime
# import random
# import re
# from django.conf import settings
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.template.loader import get_template
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .models import Buyer, Pincode
# from django.utils import simplejson

# # buyer_login


# # buyer_login
# def login(request):
#     req = request.POST.get
#     if req.get('username') and req.get('password'):







# @dajaxice_register
# def buyer_login(request, username, password, next_url=None):

#     dajax = Dajax()
#     dajax.assign('#login-error', 'innerHTML', '')
#     if username and password:
#         print username, password
#         print "Login"

#         user = authenticate(username=username, password=password)
#         print "vvvvvvvvvvvvvvvv", user

#         if user:
#             if not user.is_staff:
#                 print "login................d"
#                 login(request, user)
#                 print "login............ssssssssss"
#                 move_to_cart(request)
#                 print "after move........."
#                 if next_url:
#                     dajax.redirect(next_url)
#                 else:
#                     dajax.script('LocationReload();')
#             else:
#                 return simplejson.dumps({'status': 'warning', 'message': 'Staff can not Login here.'})
#         else:
#             print "Password Error"
#             return simplejson.dumps({'status': 'warning', 'message': 'Username & Password Not Matching'})
#     else:
#         print "Enter Valid Form"
#         return simplejson.dumps({'status': 'warning', 'message': 'Enter Valid Form.'})

#     return dajax.json()


# # # buyer_login
# # @dajaxice_register
# # def signup(request, name=None, email=None, mobile=None, pwd=None, cpwd=None, address=None, zipcode=None, city=None, country=None, state=None):

# #     dajax = Dajax()
# #     if name and email and mobile and pwd and cpwd:

# #         print name, email, mobile, pwd
# #         mobile = int(mobile)
# #         zipcode = int(zipcode)

# #         if type(mobile) and type(zipcode) == int:

# #             if User.objects.filter(email=email) or User.objects.filter(username=email):
# #                 print "######### Existing Email ###########"

# #                 return simplejson.dumps({'status': 'warning', 'message': 'A User already exist with this email address.Please select a different email address or login'})

# #             else:
# #                 if pwd != cpwd:
# #                     return simplejson.dumps({'status': 'warning', 'message': 'password mis-match please try again..'})
# #                 else:
# #                     sub = Buyer()
# #                     sub.first_name = name
# #                     sub.set_password(pwd)
# #                     sub.mobile = mobile
# #                     sub.username = email
# #                     sub.email = email
# #                     sub.street_address = address
# #                     sub.pincode = zipcode
# #                     sub.city = city
# #                     sub.country = country
# #                     sub.state = state
# #                     sub.key_generated = datetime.datetime.now()
# #                     salt = sha.new(str(random.random())).hexdigest()[:5]
# #                     sub.verification_code = sha.new(
# #                         salt + sub.email).hexdigest()
# #                     sub.save()

# #                     print "hahahah inside just click"

# #                     user = authenticate(username=sub.username, password=pwd)
# #                     if user:
# #                         login(request, user)
# #                         move_to_cart(request)

# #                         subject = 'Account created successfully'

# #                         val = {
# #                             'site_url': settings.SITE_URL,
# #                             'logo': settings.COMPANY_LOGO,
# #                             'fb': settings.COMPANY_FB_URL,
# #                             'twitter': settings.COMPANY_TWITTER_URL,
# #                             'gplus': settings.COMPANY_GPLUS_URL,
# #                             'subject': subject,
# #                             'name': name,
# #                             'mobile': mobile,
# #                             'email': email,
# #                             'username': email,
# #                             'password': pwd,
# #                             'verification_key': sub.verification_code,
# #                         }

# #                         html_content = render_to_string(
# #                             'mail/welcome.html', val)
# #                         text_content = strip_tags(html_content)

# #                         msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, to=[
# #                                                      sub.email, 'settings.DEFAULT_TO_EMAIL'])
# #                         msg.attach_alternative(html_content, "text/html")
# #                         msg.send(fail_silently=True)

# #                         print "Mail send"

# #                         dajax.script(
# #                             'Success("Your account created successfully ");')

# #                         return simplejson.dumps({'status': 'success', 'message': 'Well done! Your account created successfully. Please verify your mail id.'})

# #         else:

# #             return simplejson.dumps({'status': 'warning', 'message': 'Pincode and Phone number Must be Integear'})

# #     else:
# #         print "Enter Valid Form"
# #         return simplejson.dumps({'status': 'warning', 'message': 'Enter Valid Form.'})
# #     return dajax.json()
