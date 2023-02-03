from django.http.response import HttpResponse


def create_customer(request):
    return HttpResponse('Customer is created')


def create_user(request):
    return HttpResponse('User is registered')


def get_user(request):
    return HttpResponse('Hello user!')


def list_customers(request):
    return HttpResponse('List of customers')


def my_orders(request):
    return HttpResponse('My orders')


def address_list(request):
    return HttpResponse('List of my addresses')
