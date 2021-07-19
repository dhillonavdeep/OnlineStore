from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.forms import fields, inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unautheticated_user,allowed_users,admin_only
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

@unautheticated_user
def registerPage(request):
    form=CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # user will be set as customer(group) on registartion
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                #and it broke
            )
            #this message will be sent to login page to appear below fields
            messages.success(request,"Account has been created for "+username)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html', context)

@unautheticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username Or Password Is Incorrect')
    context={}
    return render(request,'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders= request.user.customer.order_set.all()
    print(f"Genrating page with order: {orders}")
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending= orders.filter(status='Pending').count()

    context={'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return render(request,'accounts/user.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):
    context = {}
    return render(request, 'accounts/account_settings.html', context)

def contact(request):
    return HttpResponse('Contact Page')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{'products' : products })

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {'item':order}
    return render(request,'accounts/delete.html',context)