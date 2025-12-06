from django import forms
from .models import Booking, Payment, Tour, Hotel, Transport, Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'tour', 'hotel', 'transport', 'people']
        widgets = {
            'people': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Фильтруем доступные туры
        self.fields['tour'].queryset = Tour.objects.filter(available=True)
        
        # Если пользователь авторизован, показываем только его клиента
        if user and user.is_authenticated:
            try:
                client = Client.objects.get(email=user.email)
                self.fields['client'].queryset = Client.objects.filter(id=client.id)
            except Client.DoesNotExist:
                pass

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['booking', 'amount', 'payment_method', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'booking': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            bookings = Booking.objects.filter(user=user)
            self.fields['booking'].queryset = bookings
            # Добавляем данные о сумме в опции
            self.fields['booking'].choices = [
                (booking.id, f'Бронирование #{booking.id} - {booking.tour.title} ({booking.total_price} ₽)')
                for booking in bookings
            ]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password2"):
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")