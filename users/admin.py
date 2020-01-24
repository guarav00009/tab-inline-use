from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Book,Question


from django.contrib import admin

class BookInline(admin.TabularInline):
    model = Book

class QuestionInline(admin.TabularInline):
    model = Question

class CustomUserAdmin(UserAdmin):
    inlines = [
        BookInline,QuestionInline
    ]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    list_per_page = 10  # No of records per page
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'is_staff', 'is_active','type')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class BookAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

class QuestionAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
