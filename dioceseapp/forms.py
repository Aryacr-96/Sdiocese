from django import forms
from .models import Contact, Priest, Parish
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class adminform(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


# ========================================
# PRIEST FORM - FIXED
# ========================================
class PriestForm(forms.ModelForm):

    description = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 150px;',
        }),
        label='',
        required=False
    )


    pastoral_experience = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 200px;',
        }),
        label='Pastoral Experience',
        required=False
    )


    class Meta:
        model = Priest
        fields = "__all__"

        labels = {
            'description': '',
            'pastoral_experience': 'Pastoral Experience',
        }


        widgets = {

            "ordained_on": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control-modern"
                }
            ),

            "retired_on": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control-modern"
                }
            ),


            "first_name": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter first name',
            }),


            "last_name": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter last name',
            }),


            "slug": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated from name',
                'readonly': True,
            }),


            "position": forms.Select(attrs={
                'class': 'form-control-modern',
            }),


            "home_parish": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter home parish',
            }),


            "blood_group": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'e.g., A+, O-',
            }),


            "address": forms.Textarea(attrs={
                'class': 'form-control-modern',
                'rows': 3,
                'placeholder': 'Enter residential or office address',
            }),


            "phone": forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'e.g., +1234567890',
            }),


            "email": forms.EmailInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'priest@example.com',
            }),


            "image": forms.FileInput(attrs={
                'class': 'form-control-modern',
            }),
        }
class ParishForm(forms.ModelForm):

    description = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 150px;',
        }),
        label='',
        required=False,
    )

    class Meta:
        model = Parish
        fields = [
            'name',
            'image',
            'location',
            'map_url',
            'vicar',
            'assistant_vicar',
            'established_year',
            'district',
            'phone',
            'trustee',
            'secretary',
            'number_of_families',
            'description'
        ]

        labels = {
            'description': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-modern',
            }),

            'vicar': forms.Select(attrs={
                'class': 'form-control-modern',
            }),

            'assistant_vicar': forms.Select(attrs={
                'class': 'form-control-modern',
            }),
        }


    # ADD THIS PART
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show priests in dropdown
        self.fields['vicar'].queryset = Priest.objects.all()

        self.fields['assistant_vicar'].queryset = Priest.objects.all()

        self.fields['vicar'].empty_label = "Select Vicar"

        self.fields['assistant_vicar'].empty_label = "Select Assistant Vicar"
# ========================================
# CONTACT FORM
# ========================================
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'prayer_request']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter your email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter 10-digit phone number',
                'maxlength': '10'
            }),
            'prayer_request': forms.Textarea(attrs={
                'class': 'form-control-modern',
                'rows': 5,
                'placeholder': 'Enter your prayer request'
            }),
        }