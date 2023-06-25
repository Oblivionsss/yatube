from django.shortcuts import redirect


# Проверка на авторизованность
def user_only(func):
    def check_user(request, *args, **kwargs):
        # Мы знаем, что у view-функций первый аргумент всегда request
        if not request.user.is_authenticated():
            return redirect('/auth/login')
        func(request, *args, **kwargs) 
    return check_user