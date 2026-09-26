from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .models import Certification, Education, Experience, Project, Skill


def home(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for the message. I’ll get back to you as soon as I can.",
            )
            return redirect(f"{reverse('home')}#contact")
        messages.error(request, "Please correct the errors below and try again.")

    context = {
        "form": form,
        "skills": Skill.objects.filter(is_active=True),
        "projects": Project.objects.all(),
        "experience": Experience.objects.all(),
        "education": Education.objects.all(),
        "certifications": Certification.objects.all(),
        "open_contact": request.method == "POST",
    }
    return render(request, "portfolio/index.html", context)


@require_GET
def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
