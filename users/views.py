import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser, Follow
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пользователь становится активным после подтверждения
            user.save()

            # Отправка подтверждающего письма
            current_site = get_current_site(request)
            subject = 'Подтверждение регистрации'
            message = f'''
            Привет, {user.username}!
            Пожалуйста, подтвердите свою регистрацию, перейдя по ссылке:
            http://{current_site.domain}{reverse('users:confirm_email', kwargs={'user_id': user.id})}
            '''
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [user.email], fail_silently=False)
            return redirect('users:registration_pending')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def confirm_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_email_verified:
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.success(
            request, "Регистрация успешно подтверждена! Войдите в систему.")
        return redirect('users:login')
    else:
        messages.warning(request, "Ваш email уже был подтвержден.")
        return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Все поля обязательны для заполнения.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                messages.error(request, "Неверные данные для входа.")

    return render(request, 'users/login.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    """Функция редактирования профиля"""
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен.")
            return redirect('users:profile')

    else:
        form = EditProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class FollowUserView(View):
    """Представление для подписки на пользователя."""

    def post(self, request, user_id):
        print(f"🔵 Получен запрос на подписку от {request.user} на {user_id}")
        print(f"📩 Данные запроса: {request.POST}")

        follower = request.user
        following = get_object_or_404(CustomUser, id=user_id)

        if follower == following:
            print(f"⚠️ Пользователь {follower} попытался подписаться на самого себя.")
            return JsonResponse({"error": "Нельзя подписаться на самого себя"}, status=400)

        follow, created = Follow.objects.get_or_create(follower=follower, following=following)

        if created:
            
            print(f"✅ Подписка создана: {follower} -> {following}")
        else:
            # Если подписка уже была, удаляем ее (то есть это "отписка")
            follow.delete()
            print(f"❌ Отписка: {follower} -> {following}")
            followers_count = Follow.objects.filter(following=following).count()
            return JsonResponse({"message": f"Вы отписались от {following.username}", "followers_count": followers_count}, status=200)
        # Обновляем число подписчиков
        followers_count = Follow.objects.filter(following=following).count()

        return JsonResponse({"message": f"Вы подписались на {following.username}", "followers_count": followers_count}, status=201)


@login_required
def check_follow_status(request, user_id):
    """Проверяет, подписан ли текущий пользователь на другого пользователя."""
    user_to_check = get_object_or_404(CustomUser, id=user_id)
    is_following = Follow.objects.filter(follower=request.user, following=user_to_check).exists()
    return JsonResponse({"is_following": is_following})



@method_decorator(login_required, name='dispatch')
class UnfollowUserView(View):
    """Представление для отписки от пользователя."""

    def post(self, request, user_id):
        print(f"🔴 Получен запрос на отписку от {request.user} от {user_id}")

        follower = request.user
        following = get_object_or_404(CustomUser, id=user_id)

        follow = Follow.objects.filter(follower=follower, following=following).first()

        if not follow:
            print(f"⚠️ Ошибка: {follower} не подписан на {following}")
            return JsonResponse({"error": "Вы не подписаны на этого пользователя"}, status=400)

        follow.delete()
        print(f"❌ Отписка: {follower} -> {following}")

        followers_count = Follow.objects.filter(following=following).count()
        return JsonResponse({"message": f"Вы отписались от {following.username}", "followers_count": followers_count}, status=200)
