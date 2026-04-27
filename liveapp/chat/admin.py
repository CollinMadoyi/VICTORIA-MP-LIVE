from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ChatSession,CampusNetwork

# 1. Register the Custom User
class CustomUserAdmin(UserAdmin):
    # Add your new fields (latitude, longitude) to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Location Data', {'fields': ('latitude', 'longitude')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Location Data', {'fields': ('latitude', 'longitude')}),
    )
    list_display = ['username', 'email', 'latitude', 'longitude', 'is_staff']

admin.site.register(User, CustomUserAdmin)

# 2. Register the ChatSession
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    # Use 'is_active' instead of 'active'
    # Use 'timestamp' instead of 'created_at'
    list_display = ('user1', 'user2', 'is_active', 'timestamp') 
    list_filter = ('is_active',)

@admin.register(CampusNetwork)
class CampusNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_ip')
    search_fields = ('name', 'public_ip')
