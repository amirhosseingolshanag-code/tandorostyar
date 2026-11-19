from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, BodyMeasurement, DietPreference, BodyImage

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="ایمیل")
    first_name = forms.CharField(max_length=150, label="نام")
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
        labels = {"username":"نام کاربری", "password1":"رمز عبور", "password2":"تکرار رمز عبور"}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "height_cm"]
        labels = {"age":"سن", "height_cm":"قد (سانتی‌متر)"}

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = ["weight_kg", "note"]
        labels = {"weight_kg":"وزن (کیلوگرم)", "note":"یادداشت"}

class DietForm(forms.ModelForm):
    class Meta:
        model = DietPreference
        fields = ["goal", "activity", "diet_type", "allergies"]
        labels = {"goal":"هدف", "activity":"میزان فعالیت", "diet_type":"نوع رژیم", "allergies":"حساسیت‌ها (با ویرگول جدا کنید)"}

class BodyImageForm(forms.ModelForm):
    class Meta:
        model = BodyImage
        fields = ["view", "image"]
        labels = {"view":"زاویه تصویر", "image":"انتخاب تصویر"}
        widgets = {"image": forms.ClearableFileInput(attrs={"accept":"image/*"})}
