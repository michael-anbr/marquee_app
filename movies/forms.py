from django import forms
from .models import Review, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "w-full bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-white placeholder-zinc-500 focus:outline-none focus:border-[#f5c518] transition-colors resize-none font-['Hanken_Grotesk']",
                    "placeholder": "Write your thoughts on this movie...",
                    "rows": 4,
                }
            )
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "w-full bg-zinc-900 border border-zinc-800 rounded-lg p-4 text-white placeholder-zinc-500 focus:outline-none focus:border-[#f5c518] transition-colors resize-none font-['Hanken_Grotesk']",
                    "placeholder": "Tell us about your movie tastes...",
                    "rows": 4,
                }
            ),
            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "text-sm text-zinc-400 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-zinc-800 file:text-white hover:file:bg-zinc-700 file:cursor-pointer"
                }
            ),
        }


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full bg-zinc-800 border border-zinc-700 px-4 py-2 rounded text-white text-sm focus:outline-none focus:border-[#f5c518] transition-all font-['Hanken_Grotesk']",
                }
            )
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
