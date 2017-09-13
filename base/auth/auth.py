from django.shortcuts import redirect

def check_login(func):
    def f(request,*args,**kwarsg):
        if request.session.get('login_info_user') and request.session.get('login_info_name'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/base/login.html')
