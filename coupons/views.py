from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
from django.contrib import messages


@require_POST
@login_required
def coupon_apply(request):
    action = request.POST.get('action')  # Получаем действие из кнопки
    if action == 'remove':
        # Удаляем купон из сессии
        if 'coupon_id' in request.session:
            del request.session['coupon_id']
            messages.success(request, "Kupon silindi.")
        return redirect('cart:cart_detail')

    # Обработка применения купона
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )

            # Проверяем, использовался ли купон пользователем
            if coupon.used_by_fin_codes.filter(id=request.user.id).exists():
                messages.error(request, "Bu kupon artıq istifadə edilib.")
                return redirect('cart:cart_detail')

            # Сохраняем купон в сессии
            request.session['coupon_id'] = coupon.id
            messages.success(request, "Kupon tətbiq edildi!")
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, "Kupon etibarsızdır.")

    return redirect('cart:cart_detail')
