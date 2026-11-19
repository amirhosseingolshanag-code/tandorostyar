from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from .forms import SignUpForm, ProfileForm, MeasurementForm, DietForm, BodyImageForm
from .models import UserProfile, BodyMeasurement, DietPreference, MealPlan

def home(request):
    return render(request, "core/home.html")

def signup(request):
    if request.user.is_authenticated: return redirect("dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                UserProfile.objects.create(user=user)
                DietPreference.objects.create(user=user)
            login(request, user)
            messages.success(request, "حساب کاربری شما ساخته شد.")
            return redirect("dashboard")
    else: form = SignUpForm()
    return render(request, "core/auth.html", {"form":form, "title":"ثبت‌نام", "signup":True})

@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    diet, _ = DietPreference.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(request.POST or None, instance=profile, prefix="profile")
    measure_form = MeasurementForm(request.POST or None, prefix="measure")
    diet_form = DietForm(request.POST or None, instance=diet, prefix="diet")
    image_form = BodyImageForm(request.POST or None, request.FILES or None, prefix="image")
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "profile" and profile_form.is_valid():
            profile_form.save(); messages.success(request, "پروفایل ذخیره شد.")
        elif action == "measure" and measure_form.is_valid():
            item = measure_form.save(commit=False); item.user = request.user; item.save()
            messages.success(request, "اندازه‌گیری ثبت شد.")
        elif action == "diet" and diet_form.is_valid():
            diet_form.save(); messages.success(request, "ترجیحات غذایی ذخیره شد.")
        elif action == "image" and image_form.is_valid():
            upload = image_form.save(commit=False); upload.user = request.user
            if upload.image.size > 5 * 1024 * 1024:
                messages.error(request, "حجم تصویر باید کمتر از ۵ مگابایت باشد.")
            else:
                upload.save(); messages.success(request, "تصویر بارگذاری شد.")
        elif action == "plan":
            plan = {"صبحانه":"نان سبوس‌دار، پنیر و خیار","ناهار":"مرغ یا حبوبات به‌همراه سبزیجات و غلات","میان‌وعده":"میوه و مغزها","شام":"سوپ سبزیجات و منبع پروتئین"}
            MealPlan.objects.create(user=request.user, content=plan)
            messages.info(request, "برنامه نمونه ساخته شد؛ این پیشنهاد عمومی و غیرپزشکی است.")
        return redirect("dashboard")
    latest = request.user.measurements.first()
    bmi = None
    if latest and profile.height_cm:
        h = float(profile.height_cm) / 100
        if h > 0: bmi = round(float(latest.weight_kg) / (h*h), 1)
    return render(request, "core/dashboard.html", {
        "profile_form":profile_form, "measure_form":measure_form, "diet_form":diet_form,
        "image_form":image_form, "measurements":request.user.measurements.all()[:8],
        "images":request.user.body_images.all()[:6], "plans":request.user.meal_plans.all()[:5],
        "bmi":bmi, "latest":latest,
    })
