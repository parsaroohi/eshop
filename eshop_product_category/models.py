from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    title=models.CharField(max_length=150,verbose_name='عنوان')
    name=models.CharField(max_length=150,verbose_name='عنوان در url')

    class Meta:
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'

    def __str__(self):
        return self.title