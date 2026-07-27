from django import forms
from .models import Contact, Officebearer, Priest, Parish, Spiritual
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

# forms.py
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Spiritual, Officebearer, SpiritualOfficeBearer

# ============================================
# SPIRITUAL FORM
# ============================================
class SpiritualForm(forms.ModelForm):
    """
    Form for creating/editing Spiritual categories
    """
    class Meta:
        model = Spiritual
        fields = ['category_title', 'content']
        widgets = {
            'category_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter content',
                'rows': 10
            }),
        }

    def clean_category_title(self):
        """Validate that category title is unique"""
        title = self.cleaned_data.get('category_title')
        if Spiritual.objects.filter(category_title__iexact=title).exists():
            if self.instance and self.instance.pk:
                if Spiritual.objects.filter(category_title__iexact=title).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("A spiritual category with this title already exists.")
            else:
                raise forms.ValidationError("A spiritual category with this title already exists.")
        return title


# ============================================
# OFFICE BEARER FORM
# ============================================
class OfficebearerForm(forms.ModelForm):
    """
    Form for creating/editing Office Bearers (used in office bearer management)
    """
    class Meta:
        model = Officebearer
        fields = ['name', 'designation', 'image', 'phone', 'email', 'district']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter designation'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone


# ============================================
# SPIRITUAL OFFICE BEARER FORM (For inline formset)
# ============================================
class SpiritualOfficeBearerForm(forms.ModelForm):
    """
    Form for associating office bearers with spiritual categories
    """
    officebearer = forms.ModelChoiceField(
        queryset=Officebearer.objects.all().order_by('name'),
        required=False,
        label="Select Existing Office Bearer",
        widget=forms.Select(attrs={
            'class': 'form-control office-bearer-select',
        })
    )
    
    class Meta:
        model = SpiritualOfficeBearer
        fields = ['officebearer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['officebearer'].empty_label = "-- Search or select existing --"


# ============================================
# INLINE FORMSETS
# ============================================
# Formset for editing spiritual office bearer associations
SpiritualOfficeBearerFormSet = inlineformset_factory(
    Spiritual,
    SpiritualOfficeBearer,
    form=SpiritualOfficeBearerForm,
    fields=['officebearer'],
    extra=0,  # We handle this manually in the template
    can_delete=True,
    min_num=0,
    validate_min=False,
)

# Formset for editing office bearers (used in office bearer management)
OfficebearerFormSet = modelformset_factory(
    Officebearer,
    form=OfficebearerForm,
    extra=1,
    can_delete=True,
)


# ============================================
# NEW OFFICE BEARER FORM (For creating from spiritual form)
# ============================================
class NewOfficeBearerForm(forms.ModelForm):
    """
    Form for creating new office bearers on the fly from the spiritual form
    """
    class Meta:
        model = Officebearer
        fields = ['name', 'designation', 'phone', 'email', 'district', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
                'required': False
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter designation',
                'required': False
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number',
                'required': False
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        """Validate that name is provided"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name:
            # If no name provided, this form is empty and should be ignored
            # We'll handle this in the view
            pass
        return cleaned_data


# ============================================
# NEW OFFICE BEARER FORMSET
# ============================================
NewOfficeBearerFormSet = modelformset_factory(
    Officebearer,
    form=NewOfficeBearerForm,
    extra=0,  # We handle dynamically in template
    can_delete=False,
    can_order=False,
)