from django.http import HttpResponse
from django.shortcuts import redirect

def unautheticated_user(view_func):
    #if the user is autheticated(once logged in),it redirects user to home page whenever user tries to access view with this decorator
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return view_func(request,*args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    # only allows certain roles to access a view
    # goes below login_required
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            print('Loading',request,"for",allowed_roles)
            group=None
            #default value is none when there are no groups
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                print(f'Blocked request because {group} role is not allowed to view this page!')
                return HttpResponse('You are not authorized to access this view')

        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request,*args, **kwargs):
        group=None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == "customer":
            return redirect('home')
        
        if group == "admin":
            return view_func(request,*args, **kwargs)

    return wrapper_function