from django import forms
from .models import Contact, Coordinator, Designation, Officebearer, Priest, Parish, Spiritual
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class adminform(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


# ========================================
# PRIEST FORM -
# ========================================

from django import forms
from django.core.validators import RegexValidator
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Priest, Parish
import re


class PriestForm(forms.ModelForm):

    # Phone number validator - exactly 10 digits
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message='Phone number must be exactly 10 digits and contain only numbers.',
        code='invalid_phone'
    )

    description = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 150px;',
        }),
        label='',
        required=False,
    )

    pastoral_experience = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 150px;',
        }),
        label='',
        required=False,
    )

    # Override phone field with validation
    phone = forms.CharField(
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Enter 10-digit phone number',
            'maxlength': '10',
            'pattern': '[0-9]{10}',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 10)'
        }),
        required=True,
        help_text='Enter exactly 10 digits (numbers only)'
    )

    class Meta:
        model = Priest

        fields = [
            'first_name',
            'last_name',
            'position',
            'home_parish',
            'blood_group',
            'ordained_on',
            'retired_on',
            'pastoral_experience',
            'address',
            'phone',
            'email',
            'image',
            'description'
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter first name'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter last name'
            }),

            'home_parish': forms.Select(attrs={
                'class': 'form-control-modern'
            }),

            'position': forms.Select(attrs={
                'class': 'form-control-modern'
            }),

            'blood_group': forms.Select(attrs={
                'class': 'form-control-modern'
            }),

            'ordained_on': forms.DateInput(attrs={
                'class': 'form-control-modern',
                'type': 'date'
            }),

            'retired_on': forms.DateInput(attrs={
                'class': 'form-control-modern',
                'type': 'date'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control-modern',
                'rows': 3,
                'placeholder': 'Enter address',
                'required': 'required'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'priest@example.com'
            }),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'position': 'Position',
            'home_parish': 'Home Parish',
            'blood_group': 'Blood Group',
            'ordained_on': 'Ordained On',
            'retired_on': 'Retired On',
            'pastoral_experience': 'Pastoral Experience',
            'address': 'Address',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'image': 'Photo',
            'description': 'Description',
        }

        help_texts = {
            'phone': 'Enter exactly 10 digits (numbers only)',
            'email': 'Enter a valid email address',
            'ordained_on': 'Date of ordination (Required)',
            'retired_on': 'Retirement date (Required for retired priests)',
            'address': 'Address is required',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ========================================
        # PREVENT DUPLICATE PRIEST ASSIGNMENTS
        # ========================================

        instance = kwargs.get('instance')
        all_parishes = Parish.objects.all()

        if instance and instance.pk:
            parishes_to_check = all_parishes
        else:
            parishes_to_check = all_parishes

        assigned_vicar_ids = list(
            parishes_to_check.filter(
                vicar__isnull=False
            ).values_list(
                'vicar_id',
                flat=True
            )
        )

        assigned_assistant_vicar_ids = list(
            parishes_to_check.filter(
                assistant_vicar__isnull=False
            ).values_list(
                'assistant_vicar_id',
                flat=True
            )
        )

        all_assigned_ids = list(
            set(
                assigned_vicar_ids +
                assigned_assistant_vicar_ids
            )
        )

        if instance and instance.pk:
            if instance.pk in all_assigned_ids:
                all_assigned_ids.remove(
                    instance.pk
                )

        priest_queryset = Priest.objects.all().order_by(
            'first_name',
            'last_name'
        )

        available_priests = priest_queryset.exclude(
            id__in=all_assigned_ids
        )

        if instance and instance.pk:

            available_priests = (
                available_priests |
                Priest.objects.filter(
                    pk=instance.pk
                )
            )

            available_priests = (
                available_priests
                .distinct()
                .order_by(
                    'first_name',
                    'last_name'
                )
            )

        self.available_priests = available_priests

        # ========================================
        # FIELD REQUIREMENTS
        # ========================================

        # Make ordained_on required
        self.fields['ordained_on'].required = True

        self.fields[
            'ordained_on'
        ].widget.attrs['required'] = 'required'

        # Make address required
        self.fields['address'].required = True

        self.fields[
            'address'
        ].widget.attrs['required'] = 'required'

        # Make retired_on NOT required by default
        # It will be validated in clean()
        self.fields['retired_on'].required = False

        self.fields[
            'retired_on'
        ].widget.attrs.pop(
            'required',
            None
        )

        # Make other fields optional
        optional_fields = [
            'blood_group',
            'pastoral_experience',
            'image',
            'description',
            'home_parish'
        ]

        for field in optional_fields:
            self.fields[field].required = False

    # ========================================
    # CLEAN METHODS - Validation
    # ========================================

    def clean_first_name(self):
        first_name = self.cleaned_data.get(
            'first_name'
        )

        if first_name:
            first_name = first_name.strip()

            if len(first_name) < 2:
                raise forms.ValidationError(
                    "First name must be at least 2 characters long."
                )

            if not first_name.replace(
                ' ',
                ''
            ).isalpha():
                raise forms.ValidationError(
                    "First name should contain only letters and spaces."
                )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get(
            'last_name'
        )

        if last_name:
            last_name = last_name.strip()

            if len(last_name) < 2:
                raise forms.ValidationError(
                    "Last name must be at least 2 characters long."
                )

            if not last_name.replace(
                ' ',
                ''
            ).isalpha():
                raise forms.ValidationError(
                    "Last name should contain only letters and spaces."
                )

        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get(
            'phone'
        )

        if phone:
            cleaned = re.sub(
                r'[^0-9]',
                '',
                phone
            )

            if cleaned:

                if len(cleaned) != 10:
                    raise forms.ValidationError(
                        "Phone number must be exactly 10 digits."
                    )

                return cleaned

        return phone

    def clean_email(self):
        email = self.cleaned_data.get(
            'email'
        )

        if email:
            email = email.strip().lower()

            queryset = Priest.objects.filter(
                email=email
            )

            if self.instance.pk:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise forms.ValidationError(
                    "A priest with this email already exists."
                )

        return email

    def clean_home_parish(self):
        home_parish = self.cleaned_data.get(
            'home_parish'
        )

        # Allow null/empty values
        if not home_parish:
            return None

        return home_parish

    def clean_blood_group(self):
        blood_group = self.cleaned_data.get(
            'blood_group'
        )

        if blood_group:

            valid_blood_groups = [
                'A+',
                'A-',
                'B+',
                'B-',
                'AB+',
                'AB-',
                'O+',
                'O-'
            ]

            if blood_group not in valid_blood_groups:
                raise forms.ValidationError(
                    f"Invalid blood group. Must be one of: "
                    f"{', '.join(valid_blood_groups)}"
                )

            return blood_group

        return blood_group

    def clean_ordained_on(self):
        ordained_on = self.cleaned_data.get(
            'ordained_on'
        )

        if not ordained_on:
            raise forms.ValidationError(
                "Ordination date is required."
            )

        from datetime import date

        if ordained_on > date.today():
            raise forms.ValidationError(
                "Ordination date cannot be in the future."
            )

        return ordained_on

    def clean_retired_on(self):
        """Validate retired date - Only required for retired priests"""

        retired_on = self.cleaned_data.get(
            'retired_on'
        )

        position = self.cleaned_data.get(
            'position'
        )

        ordained_on = self.cleaned_data.get(
            'ordained_on'
        )

        # Only validate if position is retired_priest
        if position == 'retired_priest':

            if not retired_on:
                raise forms.ValidationError(
                    "Retirement date is required for retired priests."
                )

            from datetime import date

            if retired_on > date.today():
                raise forms.ValidationError(
                    "Retirement date cannot be in the future."
                )

            if retired_on and ordained_on:

                if retired_on < ordained_on:
                    raise forms.ValidationError(
                        "Retirement date must be after ordination date."
                    )

        return retired_on

    # ========================================
    # ADDRESS VALIDATION
    # ========================================

    def clean_address(self):
        address = self.cleaned_data.get(
            'address'
        )

        if not address:
            raise forms.ValidationError(
                "Address is required."
            )

        address = address.strip()

        if not address:
            raise forms.ValidationError(
                "Address is required."
            )

        return address

    # ========================================
    # CLEAN
    # ========================================

    def clean(self):
        """
        Cross-field validation.

        The individual field validations are already handled
        by clean_ordained_on() and clean_retired_on().
        Keeping this empty prevents duplicate error messages.
        """

        cleaned_data = super().clean()

        return cleaned_data

    # ========================================
    # SAVE METHOD
    # ========================================

    def save(self, commit=True):

        instance = super().save(
            commit=False
        )

        if commit:

            instance.save()

            self.save_m2m()

        return instance


    
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Parish, Priest
import re
from django.core.validators import RegexValidator
from django.utils.text import slugify

class ParishForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(attrs={
            'class': 'form-control-modern',
            'style': 'width: 100%; min-height: 150px;',
            'placeholder': 'Enter a brief description or history of the parish...'
        }),
        label='',
        required=False,
    )

    # Phone field with validation
    phone = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.',
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Enter 10 digit phone number',
            'maxlength': '10',
            'pattern': '\d{10}',
            'title': 'Please enter exactly 10 digits'
        })
    )

    class Meta:
        model = Parish
        fields = [
            'name',
            'slug',
            'image',
            'location',
            'map_url',
            'vicar',
            'assistant_vicar',
            'established_year',
            'district',
            'phone',
            'whatsapp_number',
            'facebook_id',
            'facebook_url',
            'instagram_id',
            'instagram_url',
            'trustee',
            'secretary',
            'number_of_families',
            'description'
        ]

        labels = {
            'name': 'Parish Name',
            'slug': 'Slug (URL identifier)',
            'image': 'Parish Image',
            'location': 'Location',
            'map_url': 'Google Maps URL',
            'vicar': 'Vicar',
            'assistant_vicar': 'Assistant Vicar',
            'established_year': 'Established Year',
            'district': 'District',
            'phone': 'Phone Number',
            'whatsapp_number': 'WhatsApp Number',
            'facebook_id': 'Facebook ID/Username',
            'facebook_url': 'Facebook Page URL (Optional)',
            'instagram_id': 'Instagram Username',
            'instagram_url': 'Instagram Profile URL (Optional)',
            'trustee': 'Trustee',
            'secretary': 'Secretary',
            'number_of_families': 'Number of Families',
            'description': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter parish name',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Auto-generated from name (optional)',
                'help_text': 'Leave blank to auto-generate from parish name',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter location',
            }),
            'map_url': forms.URLInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'https://maps.google.com/...',
            }),
            'vicar': forms.Select(attrs={
                'class': 'form-control-modern',
            }),
            'assistant_vicar': forms.Select(attrs={
                'class': 'form-control-modern',
            }),
            'established_year': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'e.g., 1950',
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter district',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter 10 digit phone number',
                'maxlength': '10',
                'pattern': '\d{10}',
                'title': 'Please enter exactly 10 digits'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter WhatsApp number (digits only)',
                'maxlength': '15',
                'pattern': '[0-9]*',
                'title': 'Please enter only numbers',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
            }),
            'facebook_id': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'e.g., parishname or 123456789',
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'https://www.facebook.com/yourpage (optional)',
            }),
            'instagram_id': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'e.g., parishname (without @)',
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'https://www.instagram.com/yourpage/ (optional)',
            }),
            'trustee': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter trustee name',
            }),
            'secretary': forms.TextInput(attrs={
                'class': 'form-control-modern',
                'placeholder': 'Enter secretary name',
            }),
            'number_of_families': forms.NumberInput(attrs={
                'class': 'form-control-modern',
                'placeholder': '0',
            }),
        }

        help_texts = {
            'slug': 'URL-friendly version of the parish name. Leave blank to auto-generate.',
            'phone': 'Enter exactly 10 digits (e.g., 9876543210)',
            'whatsapp_number': 'Enter only numbers (no +, spaces, or special characters)',
            'facebook_id': 'Can be page ID (numbers) or username',
            'instagram_id': 'Username without the @ symbol',
            'facebook_url': 'Leave blank to auto-generate from ID',
            'instagram_url': 'Leave blank to auto-generate from username',
            'map_url': 'Paste the Google Maps share link',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ========================================
        # FILTER PRIESTS - Show ONLY active priests
        # Exclude retired_priest and seminary_student
        # Also exclude already assigned priests
        # ========================================
        
        # Get the current instance (for edit mode)
        instance = kwargs.get('instance')
        
        # Get all parishes to check which priests are already assigned
        all_parishes = Parish.objects.all()
        
        # Get IDs of priests already assigned as vicar or assistant vicar
        assigned_vicar_ids = []
        assigned_assistant_vicar_ids = []
        
        # If editing, exclude the current parish from the check
        if instance and instance.pk:
            parishes_to_check = all_parishes.exclude(pk=instance.pk)
        else:
            parishes_to_check = all_parishes
        
        # Collect IDs of priests already assigned as vicar
        assigned_vicar_ids = list(
            parishes_to_check.filter(vicar__isnull=False).values_list('vicar_id', flat=True)
        )
        
        # Collect IDs of priests already assigned as assistant vicar
        assigned_assistant_vicar_ids = list(
            parishes_to_check.filter(assistant_vicar__isnull=False).values_list('assistant_vicar_id', flat=True)
        )
        
        # Combine ALL assigned IDs (priests assigned as vicar OR assistant vicar)
        all_assigned_ids = list(set(assigned_vicar_ids + assigned_assistant_vicar_ids))
        
        # Base queryset: Only show priests with position='priest'
        priest_queryset = Priest.objects.filter(position='priest')
        
        # ========================================
        # FOR VICAR DROPDOWN:
        # Exclude priests who are already assigned as vicar OR assistant vicar
        # ========================================
        vicar_queryset = priest_queryset.exclude(id__in=all_assigned_ids)
        
        # ========================================
        # FOR ASSISTANT VICAR DROPDOWN:
        # Exclude priests who are already assigned as vicar OR assistant vicar
        # ========================================
        assistant_vicar_queryset = priest_queryset.exclude(id__in=all_assigned_ids)
        
        # ========================================
        # HANDLE EDIT MODE - Include current selection
        # ========================================
        
        # For Vicar field - Include current vicar if editing
        if instance and instance.pk and instance.vicar:
            # Add the current vicar to queryset even if they are assigned elsewhere
            vicar_queryset = vicar_queryset | Priest.objects.filter(id=instance.vicar.id)
        
        # For Assistant Vicar field - Include current assistant vicar if editing
        if instance and instance.pk and instance.assistant_vicar:
            # Add the current assistant vicar to queryset
            assistant_vicar_queryset = assistant_vicar_queryset | Priest.objects.filter(id=instance.assistant_vicar.id)
        
        # Remove duplicates and order by name
        vicar_queryset = vicar_queryset.distinct().order_by('first_name', 'last_name')
        assistant_vicar_queryset = assistant_vicar_queryset.distinct().order_by('first_name', 'last_name')
        
        # Set the filtered querysets
        self.fields['vicar'].queryset = vicar_queryset
        self.fields['assistant_vicar'].queryset = assistant_vicar_queryset

        self.fields['vicar'].empty_label = "Select Vicar"
        self.fields['assistant_vicar'].empty_label = "Select Assistant Vicar"

        # Make fields not required
        optional_fields = [
            'slug',
            'whatsapp_number', 'facebook_id', 'facebook_url', 
            'instagram_id', 'instagram_url', 'image', 'map_url',
            'phone', 'trustee', 'secretary', 'description'
        ]
        for field in optional_fields:
            self.fields[field].required = False

        # Set default for number_of_families
        self.fields['number_of_families'].required = False
        if not self.instance.pk:  # If new instance
            self.fields['number_of_families'].initial = 0

        # Exclude current vicar from assistant dropdown in edit mode
        if instance and instance.pk and instance.vicar:
            self.fields['assistant_vicar'].queryset = assistant_vicar_queryset.exclude(
                id=instance.vicar.id
            )

    # ========================================
    # CLEAN METHODS - Validation
    # ========================================
    
    def clean_slug(self):
        """Validate slug uniqueness"""
        slug = self.cleaned_data.get('slug')
        instance = self.instance
        
        if slug:
            # Clean the slug
            slug = slug.strip().lower()
            # Replace spaces with hyphens
            slug = re.sub(r'[-\s]+', '-', slug)
            # Remove any characters that aren't alphanumeric, underscore, or hyphen
            slug = re.sub(r'[^a-z0-9_-]', '', slug)
            
            # Check for uniqueness
            queryset = Parish.objects.filter(slug=slug)
            if instance.pk:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise forms.ValidationError(f'A parish with the slug "{slug}" already exists. Please choose a different slug.')
            
            return slug
        return slug

    def clean_name(self):
        """Validate and clean parish name"""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 3:
                raise forms.ValidationError("Parish name must be at least 3 characters long.")
        return name

    def clean_established_year(self):
        """Validate established year"""
        year = self.cleaned_data.get('established_year')
        if year:
            from datetime import datetime
            current_year = datetime.now().year
            if year < 1000 or year > current_year:
                raise forms.ValidationError(f"Established year must be between 1000 and {current_year}.")
        return year

    def clean_phone(self):
        """Clean phone number - only allow 10 digits"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove any non-digit characters
            cleaned = re.sub(r'[^0-9]', '', phone)
            if cleaned:
                if len(cleaned) != 10:
                    raise forms.ValidationError("Phone number must be exactly 10 digits.")
                return cleaned
        return phone

    def clean_whatsapp_number(self):
        """Clean WhatsApp number - only allow digits"""
        whatsapp = self.cleaned_data.get('whatsapp_number')
        if whatsapp:
            # Remove any non-digit characters
            cleaned = re.sub(r'[^0-9]', '', whatsapp.strip())
            if not cleaned:
                raise forms.ValidationError("Invalid WhatsApp number.")
            if len(cleaned) < 10:
                raise forms.ValidationError("WhatsApp number must be at least 10 digits.")
            if len(cleaned) > 15:
                raise forms.ValidationError("WhatsApp number cannot exceed 15 digits.")
            return cleaned
        return whatsapp

    def clean_instagram_id(self):
        """Clean Instagram username"""
        instagram = self.cleaned_data.get('instagram_id')
        if instagram:
            cleaned = instagram.strip().lstrip('@').rstrip('/')
            if len(cleaned) < 2:
                raise forms.ValidationError("Instagram username must be at least 2 characters.")
            return cleaned
        return instagram

    def clean_facebook_id(self):
        """Clean Facebook ID/username"""
        facebook = self.cleaned_data.get('facebook_id')
        if facebook:
            facebook = facebook.strip().rstrip('/')
            # If it's a full URL, extract the ID/username
            if 'facebook.com' in facebook:
                match = re.search(r'facebook\.com/(?:profile\.php\?id=)?([^/?&]+)', facebook)
                if match:
                    return match.group(1)
            # If it's a profile.php? id= format
            elif 'profile.php' in facebook:
                match = re.search(r'profile\.php\?id=([^&]+)', facebook)
                if match:
                    return match.group(1)
            return facebook
        return facebook

    def clean_map_url(self):
        """Clean Google Maps URL"""
        url = self.cleaned_data.get('map_url')
        if url:
            url = url.strip()
            # Remove pb parameter if present
            if '?pb=' in url:
                url = url.split('?pb=')[0]
            elif '&pb=' in url:
                url = url.split('&pb=')[0]
            # Remove trailing ? or &
            url = re.sub(r'[&?]+$', '', url)
            return url
        return url

    def clean_district(self):
        """Clean district name"""
        district = self.cleaned_data.get('district')
        if district:
            district = district.strip()
            if len(district) < 2:
                raise forms.ValidationError("District name must be at least 2 characters.")
            return district.title()
        return district

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        # Validate that vicar and assistant_vicar are not the same person
        vicar = cleaned_data.get('vicar')
        assistant_vicar = cleaned_data.get('assistant_vicar')
        if vicar and assistant_vicar and vicar.id == assistant_vicar.id:
            self.add_error('assistant_vicar', 'Assistant Vicar cannot be the same as Vicar.')
        
        return cleaned_data

    # ========================================
    # SAVE METHOD - Ensure slug is generated
    # ========================================
    
    def save(self, commit=True):
        """Override save to ensure slug is generated"""
        instance = super().save(commit=False)
        
        # Generate slug if not exists or if it's empty
        if not instance.slug or instance.slug == '':
            base_slug = slugify(instance.name)
            slug = base_slug
            counter = 1
            # Check for uniqueness
            while Parish.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            instance.slug = slug
        
        # Auto-set vicar_name
        if instance.vicar:
            instance.vicar_name = f"{instance.vicar.first_name} {instance.vicar.last_name}"
        elif not instance.vicar and not instance.vicar_name:
            instance.vicar_name = "No vicar assigned"
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance
    
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
from .models import Spiritual, Officebearer, SpiritualOfficeBearer, Coordinator, SpiritualCoordinator, Designation

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
            'designation': forms.Select(attrs={
                'class': 'form-control'
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
        if phone and len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')
        self.fields['designation'].empty_label = "-- Select Designation --"
        self.fields['designation'].required = False
        self.fields['designation'].help_text = "Select an official designation for this office bearer"


# ============================================
# COORDINATOR FORM
# ============================================
class CoordinatorForm(forms.ModelForm):
    """
    Form for creating/editing Coordinators
    """
    
    class Meta:
        model = Coordinator
        fields = ['name', 'designation', 'image', 'phone', 'email', 'district']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter coordinator name'
            }),
            'designation': forms.Select(attrs={
                'class': 'form-control'
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
        if phone and len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')
        self.fields['designation'].empty_label = "-- Select Designation --"
        self.fields['designation'].required = False
        self.fields['designation'].help_text = "Select an official designation for this coordinator"


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
# SPIRITUAL COORDINATOR FORM (For inline formset)
# ============================================
class SpiritualCoordinatorForm(forms.ModelForm):
    """
    Form for associating coordinators with spiritual categories
    """
    coordinator = forms.ModelChoiceField(
        queryset=Coordinator.objects.all().order_by('name'),
        required=False,
        label="Select Existing Coordinator",
        widget=forms.Select(attrs={
            'class': 'form-control coordinator-select',
        })
    )
    
    class Meta:
        model = SpiritualCoordinator
        fields = ['coordinator']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coordinator'].empty_label = "-- Search or select existing --"


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
            }),
            'designation': forms.Select(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number',
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
        if phone and len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')
        self.fields['designation'].empty_label = "-- Select Designation --"
        self.fields['designation'].required = False

    def clean(self):
        """Validate that name is provided if this form is being used"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        # If no name provided, this form is empty and should be ignored
        return cleaned_data


# ============================================
# NEW COORDINATOR FORM (For creating from spiritual form)
# ============================================
class NewCoordinatorForm(forms.ModelForm):
    """
    Form for creating new coordinators on the fly from the spiritual form
    """
    class Meta:
        model = Coordinator
        fields = ['name', 'designation', 'phone', 'email', 'district', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter coordinator name',
            }),
            'designation': forms.Select(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number',
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
        if phone and len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')
        self.fields['designation'].empty_label = "-- Select Designation --"
        self.fields['designation'].required = False

    def clean(self):
        """Validate that name is provided if this form is being used"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        # If no name provided, this form is empty and should be ignored
        return cleaned_data


# ============================================
# INLINE FORMSETS
# ============================================
# Formset for editing spiritual office bearer associations
SpiritualOfficeBearerFormSet = inlineformset_factory(
    Spiritual,
    SpiritualOfficeBearer,
    form=SpiritualOfficeBearerForm,
    fields=['officebearer'],
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False,
)

# Formset for editing spiritual coordinator associations
SpiritualCoordinatorFormSet = inlineformset_factory(
    Spiritual,
    SpiritualCoordinator,
    form=SpiritualCoordinatorForm,
    fields=['coordinator'],
    extra=0,
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

# Formset for editing coordinators (used in coordinator management)
CoordinatorFormSet = modelformset_factory(
    Coordinator,
    form=CoordinatorForm,
    extra=1,
    can_delete=True,
)

# Formset for new office bearers (from spiritual form)
NewOfficeBearerFormSet = modelformset_factory(
    Officebearer,
    form=NewOfficeBearerForm,
    extra=0,
    can_delete=False,
    can_order=False,
)

# Formset for new coordinators (from spiritual form)
NewCoordinatorFormSet = modelformset_factory(
    Coordinator,
    form=NewCoordinatorForm,
    extra=0,
    can_delete=False,
    can_order=False,
)


# ============================================
# DESIGNATION FORM
# ============================================
class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter designation name'
            }),
        }

        # forms.py
from django import forms
from django.utils.text import slugify  # <-- ADD THIS IMPORT
from .models import Karunyasparsham, Category

class KarunyasparshamForm(forms.ModelForm):
    class Meta:
        model = Karunyasparsham
        fields = [
            'content_type',
            'about_title', 'about_image', 'about_content',
            'project_title', 'project_image', 'project_description',
            'project_content', 'project_location', 'active', 'category'
        ]
        widgets = {
            'content_type': forms.Select(attrs={
                'class': 'form-control form-select',
                'id': 'contentTypeSelect',
                'onchange': 'togglePanels(this.value)'
            }),
            'about_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter about title',
                'id': 'aboutTitle'
            }),
            'about_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'aboutImageInput'
            }),
            'about_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'id': 'aboutContent'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'id': 'projectTitle'
            }),
            'project_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'projectImageInput'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter project description',
                'id': 'projectDescription'
            }),
            'project_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'id': 'projectContent'
            }),
            'project_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project location',
                'id': 'projectLocation'
            }),
            'active': forms.Select(attrs={
                'class': 'form-control form-select',
                'id': 'activeStatus'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-select',
                'id': 'categorySelect'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set category queryset
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"
        
        # Make category optional
        self.fields['category'].required = False
        
        # Set initial content type
        if self.instance and self.instance.pk:
            if self.instance.content_type:
                self.initial['content_type'] = self.instance.content_type
    
    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        
        if content_type == 'about':
            # Validate about fields
            if not cleaned_data.get('about_title'):
                self.add_error('about_title', 'About title is required for about content type')
            if not cleaned_data.get('about_content'):
                self.add_error('about_content', 'About content is required for about content type')
        elif content_type == 'project':
            # Validate project fields
            if not cleaned_data.get('project_title'):
                self.add_error('project_title', 'Project title is required for project content type')
            if not cleaned_data.get('project_content'):
                self.add_error('project_content', 'Project content is required for project content type')
            if not cleaned_data.get('project_location'):
                self.add_error('project_location', 'Project location is required for project content type')
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generate slug
        if instance.content_type == 'about' and instance.about_title:
            base_slug = slugify(instance.about_title)
        elif instance.content_type == 'project' and instance.project_title:
            base_slug = slugify(instance.project_title)
        else:
            base_slug = slugify(f"{instance.content_type}-{instance.id or 'new'}")
        
        instance.slug = instance.generate_unique_slug(base_slug)
        
        if commit:
            instance.save()
        return instance



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated from name'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
        }
        labels = {
            'name': 'Category Name',
            'slug': 'URL Slug',
            'image': 'Category Image',
        }
        help_texts = {
            'slug': 'Leave blank to auto-generate from name.',
            'image': 'Upload an image for the category (optional).',
        }


from django import forms
from .models import Publication
from django import forms
from .models import Publication
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'image', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-modern',
                'placeholder': 'Enter publication title'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-modern',
                'accept': 'image/*'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-modern',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx']
            extension = file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, Word (.doc, .docx), and Excel (.xls, .xlsx) files are allowed."
                )
            # Increase limit to 100MB
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 100MB.")
        return file

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only JPG, JPEG, PNG, GIF, and WebP images are allowed."
                )
            # Increase limit to 20MB
            if image.size > 20 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 20MB.")
        return image

# forms.py
from django import forms
from .models import Gallery

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = [
            'title', 'media_type', 'image', 
            'video_url', 'video_file', 'video_embed_code',
            'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter gallery title'
            }),
            'media_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'video_file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'video_embed_code': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Paste embed code from YouTube, Vimeo, etc.',
                'rows': 3
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description (optional)',
                'rows': 4
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the instance if it exists (for edit mode)
        instance = kwargs.get('instance')
        
        # Make image field NOT required initially
        self.fields['image'].required = False
        
        # If it's a new item (no instance), set default media type
        if not instance:
            self.fields['media_type'].initial = 'image'
        
        # If it's an existing item with an image, don't require a new image
        if instance and instance.image:
            self.fields['image'].required = False

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image = cleaned_data.get('image')
        video_url = cleaned_data.get('video_url')
        video_file = cleaned_data.get('video_file')
        video_embed_code = cleaned_data.get('video_embed_code')
        
        # Get the instance to check if it exists
        instance = getattr(self, 'instance', None)

        if media_type == 'image':
            # For image type, we need either a new image or an existing one
            if not image:
                # Check if the instance already has an image (edit mode)
                if instance and instance.image:
                    # Keep the existing image - no error
                    pass
                else:
                    # No image provided and no existing image (new item)
                    self.add_error('image', 'An image file is required when media type is Image.')
            else:
                # A new image was uploaded, validate it
                if image:
                    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
                    extension = image.name.split('.')[-1].lower()
                    if extension not in allowed_extensions:
                        self.add_error('image', 'Only JPG, JPEG, PNG, GIF, and WebP images are allowed.')
                    if image.size > 20 * 1024 * 1024:
                        self.add_error('image', 'Image size must be under 20MB.')

        elif media_type == 'video':
            # At least one of video_url, video_file, or video_embed_code must be provided
            has_video_source = video_url or video_file or video_embed_code
            
            # Check if instance already has video sources (edit mode)
            has_existing_video = False
            if instance:
                has_existing_video = instance.video_url or instance.video_file or instance.video_embed_code
            
            if not has_video_source and not has_existing_video:
                self.add_error('video_url', 'Please provide a video URL, upload a video file, or paste embed code.')
            
            # If video_url is provided, validate it
            if video_url:
                import re
                url_pattern = r'^https?://[^\s]+$'
                if not re.match(url_pattern, video_url):
                    self.add_error('video_url', 'Please enter a valid URL.')
            
            # Validate video file if uploaded
            if video_file:
                allowed_extensions = ['mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv']
                extension = video_file.name.split('.')[-1].lower()
                if extension not in allowed_extensions:
                    self.add_error('video_file', 'Only MP4, WebM, OGG, MOV, AVI, and MKV files are allowed.')
                if video_file.size > 200 * 1024 * 1024:
                    self.add_error('video_file', 'Video file size must be under 200MB.')

        return cleaned_data

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            allowed_extensions = ['mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv']
            extension = video_file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only MP4, WebM, OGG, MOV, AVI, and MKV files are allowed."
                )
            if video_file.size > 200 * 1024 * 1024:
                raise forms.ValidationError("Video file size must be under 200MB.")
        return video_file

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only JPG, JPEG, PNG, GIF, and WebP images are allowed."
                )
            if image.size > 20 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 20MB.")
        return image



#PRAYER BOOKS 

from django import forms
import os

from .models import PrayerBook


# =========================================================
# PRAYER BOOK FORM
# =========================================================

class PrayerBookForm(forms.ModelForm):

    class Meta:

        model = PrayerBook

        fields = [
            'title',
            'image',
            'file'
        ]

        widgets = {

            # -----------------------------------------
            # TITLE
            # -----------------------------------------

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter prayer book title'
                }
            ),

            # -----------------------------------------
            # COVER IMAGE
            # -----------------------------------------

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                    'accept': 'image/*'
                }
            ),

            # -----------------------------------------
            # PDF FILE
            # -----------------------------------------

            'file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                    'accept': '.pdf,application/pdf'
                }
            ),
        }

    # =====================================================
    # IMAGE VALIDATION
    # =====================================================

    def clean_image(self):

        image = self.cleaned_data.get(
            'image'
        )

        if not image:

            return image

        allowed_extensions = [
            'jpg',
            'jpeg',
            'png',
            'gif',
            'webp'
        ]

        extension = os.path.splitext(
            image.name
        )[1].lower().replace(
            '.',
            ''
        )

        if extension not in allowed_extensions:

            raise forms.ValidationError(
                "Only JPG, JPEG, PNG, GIF, and WebP "
                "images are allowed."
            )

        return image

    # =====================================================
    # PDF FILE VALIDATION
    # =====================================================

    def clean_file(self):

        file = self.cleaned_data.get(
            'file'
        )

        if not file:

            return file

        # -----------------------------------------
        # CHECK EXTENSION
        # -----------------------------------------

        extension = os.path.splitext(
            file.name
        )[1].lower()

        if extension != '.pdf':

            raise forms.ValidationError(
                "Only PDF files are allowed."
            )

        # -----------------------------------------
        # CHECK MIME TYPE
        # -----------------------------------------

        content_type = getattr(
            file,
            'content_type',
            None
        )

        if content_type != 'application/pdf':

            raise forms.ValidationError(
                "Only PDF files are allowed."
            )

        # -----------------------------------------
        # CHECK ACTUAL PDF CONTENT
        # -----------------------------------------

        try:

            file.seek(0)

            header = file.read(5)

            file.seek(0)

            if header != b'%PDF-':

                raise forms.ValidationError(
                    "The uploaded file is not a valid PDF."
                )

        except forms.ValidationError:

            raise

        except Exception:

            raise forms.ValidationError(
                "Unable to validate the uploaded PDF file."
            )

        return file




#KALPANA
from django import forms
from django.core.exceptions import ValidationError
from .models import Kalpana, KalpanaFile
import os


class KalpanaForm(forms.ModelForm):
    """Form for creating/editing Kalpana"""

    class Meta:
        model = Kalpana
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Kalpana 2026, Kalpana 2025'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError(
                'Title must be at least 5 characters long.'
            )
        return title



class KalpanaFileForm(forms.ModelForm):
    """Form for uploading a single PDF file with description"""

    class Meta:
        model = KalpanaFile
        fields = ['file', 'file_name', 'description']

        widgets = {
            'file': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'application/pdf,.pdf'
                }
            ),

            'file_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Display name for the file (optional)'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Enter description for this file...'
                }
            ),
        }

    def clean_file(self):

        file = self.cleaned_data.get('file')

        if not file:
            return file

        # 1. Check extension
        ext = os.path.splitext(file.name)[1].lower()

        if ext != '.pdf':
            raise ValidationError(
                'Only PDF files are allowed.'
            )

        # 2. Check MIME type
        content_type = getattr(
            file,
            'content_type',
            None
        )

        if content_type != 'application/pdf':
            raise ValidationError(
                'Only PDF files are allowed.'
            )

        # 3. Check actual PDF signature
        try:
            file.seek(0)

            header = file.read(5)

            file.seek(0)

            if header != b'%PDF-':
                raise ValidationError(
                    'The uploaded file is not a valid PDF.'
                )

        except ValidationError:
            raise

        except Exception:
            raise ValidationError(
                'Unable to validate the uploaded file.'
            )

        return file




class KalpanaWithFilesForm(forms.ModelForm):
    """Combined form for Kalpana with multiple files (used in template)"""

    class Meta:
        model = Kalpana
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Kalpana 2026, Kalpana 2025'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError(
                'Title must be at least 5 characters long.'
            )
        return title


class KalpanaUpdateForm(forms.ModelForm):
    """Form for updating Kalpana with existing files"""

    class Meta:
        model = Kalpana
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Kalpana 2026, Kalpana 2025'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError(
                'Title must be at least 5 characters long.'
            )
        return title


class KalpanaFileUpdateForm(forms.ModelForm):
    """Form for updating an existing file's description"""

    class Meta:
        model = KalpanaFile
        fields = ['file_name', 'description']
        widgets = {
            'file_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display name for the file'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter description for this file...'
            }),
        }



# EVENTS FORM

from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'event_time', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your event in detail...',
                'required': True,
            }),
            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True,
            }),
            'event_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter venue or location',
                'required': True,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        labels = {
            'title': 'Event Title',
            'description': 'Description',
            'event_date': 'Event Date',
            'event_time': 'Event Time',
            'location': 'Location',
            'image': 'Event Image',
        }
        help_texts = {
            'image': 'Recommended: 800×600 pixels. Max 5MB.',
        }

    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        event_time = cleaned_data.get('event_time')
        
        if event_date and event_time:
            import datetime
            # Combine date and time
            event_datetime = datetime.datetime.combine(event_date, event_time)
            
            # Make it timezone-aware using Django's timezone
            event_datetime = timezone.make_aware(event_datetime)
            
            # Now compare with timezone.now() which is also aware
            if event_datetime < timezone.now():
                raise forms.ValidationError(
                    "Event date and time cannot be in the past. Please select a future date and time."
                )
        
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be less than 5MB.")
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file format. Please use: {', '.join(valid_extensions)}"
                )
        return image


#DOWNLOADS



from django import forms
from .models import Download
class DownloadForm(forms.ModelForm):
    class Meta:
        model = Download
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx',
            }),
        }
        labels = {
            'document_type': 'Document Type',
            'file': 'Upload File',
        }
        help_texts = {
            'document_type': 'Select the type of document',
            'file': 'Supported formats: PDF, Word (DOC/DOCX), Excel (XLS/XLSX)',
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            # Get selected document type
            document_type = self.cleaned_data.get('document_type')

            # Get file extension
            extension = file.name.split('.')[-1].lower()

            # Church Account Manual - PDF ONLY
            if document_type == 'church_account_manual':
                valid_extensions = ['pdf']

            # 1934 Constitution - PDF ONLY
            elif document_type == 'constitution_1934':
                valid_extensions = ['pdf']

            # Guidelines - EXCEL ONLY
            elif document_type == 'guidelines':
                valid_extensions = ['xls', 'xlsx']

            # Other document types
            else:
                valid_extensions = [
                    'pdf',
                    'doc',
                    'docx',
                    'xls',
                    'xlsx'
                ]

            if extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file format. Please use: "
                    f"{', '.join(valid_extensions)}"
                )

        return file



# SYNOD

from django import forms
from .models import Synod
import re


class SynodForm(forms.ModelForm):

    class Meta:
        model = Synod

        fields = [
            'name',
            'image',
            'description',
            'content',
            'address',
            'phone_numbers',
            'email',
            'facebook',
            'instagram',
            'slug',
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Synod name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter short description',
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter address',
            }),

            'phone_numbers': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '["9876543210", "9847012345"]',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),

            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.facebook.com/yourpage',
            }),

            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.instagram.com/yourpage',
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter slug',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


    def clean_phone_numbers(self):

        phone_numbers = self.cleaned_data.get('phone_numbers')

        if not phone_numbers:
            return []

        if not isinstance(phone_numbers, list):
            raise forms.ValidationError(
                'Please enter phone numbers as a JSON list.'
            )

        for phone in phone_numbers:

            # Convert number to string
            phone = str(phone).strip()

            # Must contain only digits
            if not phone.isdigit():
                raise forms.ValidationError(
                    f'{phone} must contain numbers only.'
                )

            # Must be exactly 10 digits
            if len(phone) != 10:
                raise forms.ValidationError(
                    f'{phone} must contain exactly 10 digits.'
                )

            # Indian mobile numbers should start with 6, 7, 8 or 9
            if phone[0] not in '6789':
                raise forms.ValidationError(
                    f'{phone} is not a valid Indian mobile number.'
                )

        return phone_numbers