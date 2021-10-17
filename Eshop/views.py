import itertools

from django.shortcuts import redirect,render

from eshop_products.models import Product
from eshop_sliders.models import Slider
from eshop_settings.models import SiteSettings
from utilities.MailService import EmailService


def header(request,*args,**kwargs):
    site_setting = SiteSettings.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request,"shared/Header.html",context)


def footer(request,*args,**kwargs):
    site_setting=SiteSettings.objects.first()
    context={
        'setting':site_setting
    }
    return render(request,"shared/Footer.html",context)


def mygrouper(n, iterable):
    # group list to list
    args=[iter(iterable)]*n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def home_page(request):
    sliders=Slider.objects.all()
    most_visit_products=Product.objects.order_by('-visit_count').all()[:8]
    latest_products=Product.objects.order_by('-id').all()[:8]
    EmailService.send_email('ارسال ایمیل تست',['test123@gmail.com'],'emails/test_email.html',{
        'title':'این یک پیام تستی می باشد.',
        'description':'این یک پیام تستی از سایت فروشگاهی ساخته شده توسط فریمورک جنگو است.'
    })
    context = {
        'data':'new data',
        'sliders':sliders,
        'most_visit':mygrouper(4,most_visit_products),
        'latest_products':mygrouper(4,latest_products)
    }
    return render(request,"home_page.html",context)


def about_page(request):
    site_setting = SiteSettings.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request,'about_page.html',context)


def handle_404_error(request, exception):
    return render(request,'404.html',{})