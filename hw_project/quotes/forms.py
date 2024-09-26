from django.forms import ModelForm, CharField, DateField, TextInput, DateInput, Textarea
from django import forms

from .models import Author, Tag, Quote


class DateInput(DateInput):
    input_type = "date"


class AuthorForm(forms.ModelForm):
    full_name = forms.CharField(
        min_length=2,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                # "placeholder": "Input full_name",
            }
        ),
    )
    born_date = DateField(
        required=True,
        widget=DateInput(
            attrs={
                "class": "form-control",
                # "placeholder": "Input born date",
            }
        ),
    )
    born_location = forms.CharField(
        min_length=2,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                # "placeholder": "Input born location",
            }
        ),
    )
    description = forms.CharField(
        min_length=10,
        max_length=10000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                # "placeholder": "Input description",
            }
        ),
    )

    class Meta:
        model = Author
        fields = ["full_name", "born_date", "born_location", "description"]


class QuoteForm(forms.ModelForm):
    quote = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "5"})
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all().order_by("full_name"),
        empty_label=" -- select an option -- ",
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("title"),
        widget=forms.SelectMultiple(
            attrs={
                "size": "12",
            },
        ),
    )

    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]


class TagForm(ModelForm):
    title = CharField(min_length=1, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["title"]