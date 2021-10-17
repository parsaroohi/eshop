from django.shortcuts import render

from eshop_settings.models import SiteSettings
from .models import ContactUs

# Create your views here.
from eshop_contact.forms import CreateContactForm


def contact_page(request):
    contact_form = CreateContactForm(request.POST or None)

    if contact_form.is_valid():
        full_name=contact_form.cleaned_data.get('full_name')
        email = contact_form.cleaned_data.get('email')
        subject = contact_form.cleaned_data.get('subject')
        text = contact_form.cleaned_data.get('text')

        ContactUs.objects.create(full_name,email,subject,text,is_read=False)
        # todo: show user a success message
        contact_form=CreateContactForm()


    setting=SiteSettings.objects.first()

    context={
        'contact-form':contact_form,
        'setting':setting
    }
    return render(request,'contacts/contact_us_page.html',context)