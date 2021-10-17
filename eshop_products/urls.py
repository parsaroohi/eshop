from django.urls import path
from .views import ProductList,product_detail,SearchProductsView,ProductListByCategory,products_category


urlpatterns = [
    path('products/',ProductList.as_view()),
    path('products/<category_name>',ProductListByCategory.as_view()),
    path('products/<productId>/<name>',product_detail),
    path('products/search',SearchProductsView.as_view()),
    path('product_categories_partial',products_category,name='products_categories')
]
