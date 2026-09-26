from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
        label="Website",
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your name",
                    "autocomplete": "name",
                    "maxlength": "120",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "What would you like to build?",
                    "rows": 6,
                    "maxlength": "4000",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "website":
                field.widget.attrs["class"] = "hp-field"
                continue
            css = "form-control"
            if self.errors.get(name):
                css += " is-invalid"
            field.widget.attrs["class"] = css
            field.widget.attrs["aria-invalid"] = "true" if self.errors.get(name) else "false"

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 12:
            raise forms.ValidationError("Please write a short message (at least 12 characters).")
        if len(message) > 4000:
            raise forms.ValidationError("Message is too long.")
        return message

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Unable to send this message.")
        return cleaned
