from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class SiteProfile(models.Model):
    """
    Singleton site identity. Edit in Django Admin instead of changing templates.

    Replace the seeded placeholder values with your own name, bio, photo, and links.
    """

    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=160, default="Python Developer")
    short_intro = models.TextField(
        help_text="One or two sentences shown in the hero section."
    )
    about_text = models.TextField(help_text="Longer About Me copy. Use line breaks for paragraphs.")
    career_summary = models.TextField(
        blank=True,
        help_text="Short career/learning summary shown beside the about copy.",
    )
    location = models.CharField(max_length=120, blank=True)
    availability = models.CharField(
        max_length=160,
        blank=True,
        help_text="Example: Open to backend roles and freelance Django work.",
    )
    email = models.EmailField()
    github_url = models.URLField()
    linkedin_url = models.URLField()
    resume_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Browser and SEO title. Defaults to name + headline.",
    )
    meta_description = models.CharField(max_length=160)
    og_image = models.ImageField(
        upload_to="og/",
        blank=True,
        help_text="Optional Open Graph image. Falls back to the profile image.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.full_name

    def clean(self):
        if not self.pk and SiteProfile.objects.exists():
            raise ValidationError("Only one site profile is allowed. Edit the existing record.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def seo_title(self):
        return self.meta_title or f"{self.full_name} — {self.headline}"

    @property
    def initials(self):
        parts = [part for part in self.full_name.split() if part]
        if not parts:
            return "PD"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return f"{parts[0][0]}{parts[-1][0]}".upper()

    @classmethod
    def get_solo(cls):
        profile = cls.objects.first()
        if profile:
            return profile
        return cls(
            full_name="Jordan Hale",
            headline="Python Developer",
            short_intro="I build reliable Django applications, clean APIs, and production-ready backends.",
            about_text="",
            email="hello@jordanhale.dev",
            github_url="https://github.com/your-username",
            linkedin_url="https://www.linkedin.com/in/your-username/",
            meta_description="Python and Django developer portfolio.",
        )


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("language", "Language"),
        ("framework", "Framework"),
        ("frontend", "Frontend"),
        ("data", "Data"),
        ("tooling", "Tooling"),
    ]

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="tooling")
    summary = models.CharField(max_length=180, blank=True)
    icon_key = models.CharField(
        max_length=40,
        help_text="CSS icon key, e.g. python, django, git. Used by the frontend sprite.",
    )
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField()
    technologies = models.CharField(
        max_length=255,
        help_text="Comma-separated list, e.g. Django, PostgreSQL, HTMX",
    )
    image = models.ImageField(upload_to="projects/", blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField("Live demo URL", blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "display_order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tech_list(self):
        return [item.strip() for item in self.technologies.split(",") if item.strip()]


class Experience(models.Model):
    role = models.CharField(max_length=140)
    organization = models.CharField(max_length=160)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Leave blank if this is your current role.",
    )
    description = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role} · {self.organization}"

    @property
    def is_current(self):
        return self.end_date is None


class Education(models.Model):
    credential = models.CharField(max_length=160)
    institution = models.CharField(max_length=160)
    field_of_study = models.CharField(max_length=160, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_year"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.credential} · {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=180)
    issuer = models.CharField(max_length=160)
    year = models.PositiveSmallIntegerField()
    credential_url = models.URLField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-year"]

    def __str__(self):
        return f"{self.title} · {self.issuer}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
