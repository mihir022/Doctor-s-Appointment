from django.contrib import admin
from .models import Doctor, Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["doctor", "pincode", "state", "city", "street", "address", "contact", "email", "age", "lastname", "firstname", "user"][::-1]

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["name"]
