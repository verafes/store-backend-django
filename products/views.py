from django.http.response import HttpResponse


def add_product(request):
    return HttpResponse('New product added')


def get_product(request):
    return HttpResponse('Product')


def product_list(request):
    return HttpResponse('Last of all products')


def category_list(request):
    return HttpResponse('List of categories')


def get_category(request):
    return HttpResponse('Category')


def brand_list(request):
    return HttpResponse('List of brands')


def get_brand(request):
    return HttpResponse('Brand')
