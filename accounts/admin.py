from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","name","mobile_no", "email","is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User credential', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name" , "mobile_no"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    # yha pe wo chize likhni hai jjo user ko display 
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [ "name" ,"mobile_no","email",  "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email" , "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
