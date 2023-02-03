from django.http.response import HttpResponse


def order_list(request):
    return HttpResponse('My orders')


def update_cart(request):
    return HttpResponse('Products added to cart')


def cart_list(request):
    return HttpResponse('List of Products in cart')


def checkout(request):
    return HttpResponse('Add shipping address and place order')