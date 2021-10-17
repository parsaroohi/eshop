from django.contrib import admin

# Register your models here.
from eshop_settings.models import SiteSettings

admin.site.register(SiteSettings)
