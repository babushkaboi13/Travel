from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Tour, Client, Booking, Payment
from .forms import RegisterForm, LoginForm, BookingForm, PaymentForm

def home(request):
    tours = Tour.objects.filter(available=True)
    return render(request, 'main/home.html', {'tours': tours})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, id=pk)
    return render(request, 'main/tour_detail.html', {'tour': tour})

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.total_price = booking.tour.price * booking.people
            booking.save()
            messages.success(request, 'Бронирование успешно создано!')
            return redirect('main:profile')
    else:
        form = BookingForm(user=request.user)
    
    return render(request, 'main/booking_form.html', {'form': form})

def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оплата успешно проведена!')
            return redirect('main:home')
    else:
        form = PaymentForm()
    
    return render(request, 'main/payment_form.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # создаем Client автоматически
            Client.objects.create(
                full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                email=user.email,
                phone="-",
                passport_number="-",
                birth_date="2000-01-01",
                address="Не указано"
            )

            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect("main:login")  # Исправлено здесь

    else:
        form = RegisterForm()
    
    return render(request, "main/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect("main:profile")  # Исправлено здесь
    else:
        form = LoginForm()
    
    return render(request, "main/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect("main:login")  # Исправлено здесь

@login_required
def profile(request):
    try:
        client = Client.objects.get(email=request.user.email)
    except Client.DoesNotExist:
        # Создаем клиента, если его нет
        client = Client.objects.create(
            full_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            email=request.user.email,
            phone="-",
            passport_number="-",
            birth_date="2000-01-01",
            address="Не указано"
        )
    
    bookings = Booking.objects.filter(user=request.user)
    
    return render(request, "main/profile.html", {
        "client": client,
        "bookings": bookings
    })

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "main/booking_detail.html", {"booking": booking})