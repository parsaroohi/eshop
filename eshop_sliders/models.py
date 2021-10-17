from django.db import models
import os
import random
# Create your models here.

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext


def upload_image_path(instance,filename):
    new_name=random.randint(1,27634723542)
    name,ext=get_filename_ext(filename)
    final_name=f"{instance.id}-{instance.title}{ext}"
    return f"sliders/{final_name}"


class Slider(models.Model):
    title=models.CharField(max_length=150,verbose_name='عنوان')
    link=models.URLField(max_length=100,verbose_name='آدرس')
    description=models.TextField(verbose_name='توضیحات')
    image=models.ImageField(upload_to=upload_image_path,null=True,blank=True,verbose_name='تصویر')

    class Meta:
        verbose_name='اسلایدر'
        verbose_name_plural='اسلایدرها'

    def __str__(self):
        return self.title