from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from account.forms import UserRegisterForm, ProfileForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import get_user_model

from orders.models import Order

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'{email} üçün hesab uğurla yaradıldı!')
            return redirect('account:login')
        else:
            messages.error(request, 'Qeydiyyatınızla bağlı xəta baş verdi. Zəhmət olmasa formanı yoxlayın.')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'account/registration.html', context=context)


class VerifyEmailView(View):
    def get(self, request):
        token = request.GET.get('token')
        if token:
            user = User.objects.filter(verification_token=token).first()
            if user:
                if user.is_verified:
                    return render(request, 'account/email_verification.html',
                                  {'message': 'E-poçt ünvanı artıq təsdiqlənib.'})
                else:
                    user.is_verified = True
                    user.is_active = True  # Устанавливаем пользователя активным после подтверждения
                    user.save()
                    return render(request, 'account/email_verification.html',
                                  {'message': 'E-poçt ünvanı uğurla təsdiqləndi.'})
            else:
                return render(request, 'account/email_verification.html', {'message': 'Yanlış token.'})
        else:
            return HttpResponseBadRequest("Token yoxdur.")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"Xöş gəldiniz {user.first_name} {user.last_name}")
                return redirect('shop:index')
            else:
                messages.error(request, f"Xəta: İstifadəçi adı və ya şifrə yalışdır! Məlumatları bir daha yoxlayın.")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


# @login_required
# def profile(request):
#     user = request.user  # Получаем текущего пользователя
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('account:profile')
#     else:
#         form = ProfileForm(instance=user)  # Предварительно заполняем форму данными текущего пользователя
#     context = {'form': form}
#     return render(request, 'account/profile.html', context=context)


@login_required
def profile(request):
    user = request.user  # Получаем текущего пользователя
    orders = Order.objects.filter(user=user)  # Получаем заказы текущего пользователя

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Сохраняем профиль
            form.save()

            # Обрабатываем изменение пароля
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            if old_password and new_password:
                if not user.check_password(old_password):
                    messages.error(request, "Cari şifrə səhv daxil edilib.")
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Şifrə uğurla dəyişdirildi.")

            messages.success(request, "Profiliniz yeniləndi!")
            return redirect('account:profile')
    else:
        form = ProfileForm(instance=user)  # Предварительно заполняем форму данными текущего пользователя

    context = {
        'form': form,
        'orders': orders,  # Добавляем заказы в контекст
    }
    return render(request, 'account/profile.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('shop:index')
