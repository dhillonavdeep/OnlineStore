from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.forms import fields, inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
    form=CreateUserForm()
    
    if request.method == 'POST':
        print("RQST->",request.META)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,"Account was created for "+user)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html', context)

def loginPage(request):
    if request.method == "POST":
        request.POST.get('username')
        request.POST.get('password')
    context={}
    return render(request,'accounts/login.html', context)

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers,
   'total_customers': total_customers,'total_orders':total_orders,
    'delivered':delivered,'pending':pending} 

    return render(request,'accounts/dashboard.html',context)

def contact(request):
    return HttpResponse('Contact Page')

def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{'products' : products })

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count=orders.count()

    customerFilter = OrderFilter(request.GET,queryset=orders)
    #customerFilter takes GEt data and queryset it filters
    orders = customerFilter.qs
    #we rebuilds orders variable

    context={'customer':customer,'orders':orders,'order_count':order_count,'customerFilter':customerFilter}
    
    return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    #extra sets how many objects show at once
    #when calling parent goes first
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # Order.objects.none() removes orders which are already placed(removes all existing objects)
    # form = OrderForm(initial={'customer':customer})
    context= {'formset':formset}
    if request.method == 'POST':
        print('PRINTING POST:',request.POST)
        # form = OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk) # gets id from GET request
    form = OrderForm(instance=order)
    context={'form':form}
    # it is broken because it uses form instef of formset(which our template expects)
    if request.method == 'POST':
        #print('PRINTING POST:',request.POST)
        form = OrderForm(request.POST,instance=order)
        #normal request.POST will create a new instance but using instance we specify which specific one to change
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {'item':order}
    return render(request,'accounts/delete.html',context)