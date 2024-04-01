from django.contrib import admin
from .models import Customer, Order, Category, Product, Profile
from django.contrib.auth.models import User

admin.site.register([Customer, Order, Product, Category, Profile])

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)