from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# 因为在views.py使用了类的形式来进行开发，所以方法@login_required不能直接作用在类上，
# 所以参考网上类装饰器使用，写了如下类来继承，进行对用户登录权限的控制


class LoginRequiredMixin(object):
    # method_decorator装饰器将函数装饰器转换成方法装饰器，这样它就可以用于实例方法

    @method_decorator(login_required(login_url='/login/'))
    # 使用dispatch回调函数
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


