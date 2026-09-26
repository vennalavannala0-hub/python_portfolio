from django.contrib import admin

from .models import (
    Certification,
    ContactMessage,
    Education,
    Experience,
    Project,
    SiteProfile,
    Skill,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Identity",
            {"fields": ("full_name", "headline", "location", "availability", "profile_image")},
        ),
        ("Copy", {"fields": ("short_intro", "about_text", "career_summary")}),
        ("Links", {"fields": ("email", "github_url", "linkedin_url", "resume_url")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "icon_key", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "summary")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "display_order", "github_url")
    list_editable = ("is_featured", "display_order")
    list_filter = ("is_featured",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "technologies")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "start_date", "end_date", "display_order")
    list_editable = ("display_order",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("credential", "institution", "start_year", "end_year", "display_order")
    list_editable = ("display_order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "year", "display_order")
    list_editable = ("display_order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")
    list_editable = ("is_read",)

    def has_add_permission(self, request):
        return False
