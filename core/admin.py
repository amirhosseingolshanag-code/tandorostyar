from django.contrib import admin
from .models import UserProfile, BodyMeasurement, DietPreference, BodyImage, MealPlan
admin.site.register([UserProfile, BodyMeasurement, DietPreference, BodyImage, MealPlan])
