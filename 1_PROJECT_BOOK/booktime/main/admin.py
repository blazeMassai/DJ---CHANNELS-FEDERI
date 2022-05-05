from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import (
    UserAdmin as DjangoUserAdmin
)
# from django.contrib.auth.models import User
from .models import *


# Register your models here.
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description', 'active')
    list_filter = ('active',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'slug', 'active', 'in_stock')
    list_filter = ('active', 'in_stock', 'date_updated')
    list_editable = ('in_stock',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ('tags',)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'image', 'thumbnail')
    readonly_fields = ('thumbnail',)
    search_fields = ('product_name',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"/>' % obj.thumbnail.url
            )
        return "-"

    thumbnail_tag.short_description = "Thumbnail"

    def product_name(self, obj):
        return obj.product.name


class CustomUserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
        (
            "Important Dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "address1",
        "address2",
        "city",
        "country",
    )
    readonly_fields = ("user",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Address, AddressAdmin)
