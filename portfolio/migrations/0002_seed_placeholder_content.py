from django.db import migrations


def load_placeholder_content(apps, schema_editor):
    from portfolio.seed import seed_portfolio

    seed_portfolio()


def unload_placeholder_content(apps, schema_editor):
    for model_name in (
        "Certification",
        "Education",
        "Experience",
        "Project",
        "Skill",
        "SiteProfile",
    ):
        apps.get_model("portfolio", model_name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_placeholder_content, unload_placeholder_content),
    ]
