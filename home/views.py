from django.shortcuts import render
from buyer.models import Buyer
from home.forms import BuyerCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from home.tokens import account_activation_token
from django.core.mail import EmailMessage
from product.models import Products
from django.contrib.auth.decorators import login_required

def home(request):
    latest_products = Products.objects.order_by('-date')[:8]
    hot_products = Products.objects.filter(is_hot=True).order_by('-date')[:8]
    featured_products = Products.objects.filter(is_featured=True).order_by('-date')[:8]
    return render(
        request, 'home/home.html', 
        {
            'lp': latest_products, 
            'hp': hot_products,
            'fp': featured_products })




def register(request):
    form = BuyerCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        current_site = get_current_site(request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('mailtemp/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()
        messages.success(request, "Your Account is created successfully, \
                Please check your email for verification link to activate your account")
        return redirect('account_activation_sent')
    return render(request, 'registration/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'mailtemp/account_activation.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Buyer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Buyer.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        login(request, user)
        messages.success(request, "Thank you, User email Successfully verified")
        return redirect('home')
    else:
        messages.warning(request, "Token expired/User does't not exist's")
        return redirect('account_activation_sent')
