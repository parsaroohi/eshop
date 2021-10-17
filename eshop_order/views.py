import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
import requests
import json
from zeep import Client

# Create your views here.
from eshop_order.forms import UserNewOrderForm
from eshop_order.models import Order, OrderDetail
from eshop_products.models import Product


@login_required(login_url='/login')
def add_user_order(request):
    new_order_form=UserNewOrderForm(request.POST or None)
    if new_order_form.is_valid():
        order=Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
        if order is None:
            order=Order.objects.create(owner_id=request.user.id,is_paid=False)

        productId = new_order_form.cleaned_data.get('productId')
        count = new_order_form.cleaned_data.get('count')
        if count<0:
            count=1
        product=Product.objects.get_by_id(productId)

        order.orderdetail_set.create(product_id=product.id,price=product.price,count=count)
        # todo: redirect user to user panel
        # return redirect('/user/orders')
        return redirect(f'/products/{product.id}/{product.title.replace(" ","-")}')

    return redirect('/')


@login_required(login_url='/login')
def user_open_order(request,*args,**kwargs):
    context={
        'order':None,
        'details':None,
        'total':0
    }
    open_order: Order =Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context['order']=open_order
        context['details']=open_order.orderdetail_set.all()
        context['total']=open_order.get_total_price()

    return render(request,'order/user_open_order.html',context)


@login_required(login_url='/login')
def remove_order_detail(request,*args,**kwargs):
    detail_id=kwargs.get('detail_id')
    if detail_id is not None:
        order_detail =OrderDetail.objects.get_queryset().get(id=detail_id,order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
            return redirect('/open-order')
    raise Http404()


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# Important: need to edit for really server.
#client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify/'


def send_request(request,*args,**kwargs):
    total_price=0
    open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    if open_order is not None:
        total_price = open_order.get_total_price()
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price,
            "callback_url": f'{CallbackURL}/{open_order.id}',
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    raise Http404()


def verify(request,*args,**kwargs):
    orderId=kwargs.get('order_id')
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                user_order=Order.objects.get_queryset().get(id=orderId)
                user_order.is_paid=True
                user_order.payment_date=time.time()
                user_order.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')