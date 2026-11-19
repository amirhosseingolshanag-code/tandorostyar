from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"پروفایل {self.user.username}"

class BodyMeasurement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="measurements")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    measured_at = models.DateField(auto_now_add=True)
    note = models.CharField(max_length=250, blank=True)
    class Meta: ordering = ["-measured_at", "-id"]
    def __str__(self): return f"{self.user.username} - {self.weight_kg} kg"

class DietPreference(models.Model):
    DIET_CHOICES = [("normal","معمولی"),("vegetarian","گیاه‌خواری"),("vegan","وگان"),("low_carb","کم‌کربوهیدرات")]
    ACTIVITY_CHOICES = [("low","کم"),("medium","متوسط"),("high","زیاد")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diet_preference")
    goal = models.CharField(max_length=20, choices=[("lose","کاهش وزن"),("maintain","حفظ وزن"),("gain","افزایش وزن")], default="maintain")
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default="medium")
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES, default="normal")
    allergies = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class BodyImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="body_images")
    image = models.ImageField(upload_to="body_images/")
    view = models.CharField(max_length=20, choices=[("front","روبرو"),("left","چپ"),("right","راست")])
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MealPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meal_plans")
    title = models.CharField(max_length=120, default="برنامه غذایی نمونه")
    content = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
