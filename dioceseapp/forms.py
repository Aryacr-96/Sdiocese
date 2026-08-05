from django import forms
from .models import Contact, Coordinator, Designation, Officebearer, Priest, Parish, Spiritual
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

# forms.py

from django import forms
from .models import Officebearer


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
            # ✅ Changed from TextInput to Select
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
        # Set the queryset for designation dropdown
        from .models import Designation
        self.fields['designation'].queryset = Designation.objects.all().order_by('name')
        self.fields['designation'].empty_label = "-- Select Designation --"
        self.fields['designation'].required = False
        self.fields['designation'].help_text = "Select an official designation for this office bearer"


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



# ============================================
# COORDINATOR FORM (With FK to Designation)
# ============================================
class CoordinatorForm(forms.ModelForm):
    """
    Form for creating/editing Coordinators with designation dropdown
    """
    # ✅ Designation as ModelChoiceField (Dropdown)
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all().order_by('name'),
        empty_label="-- Select Designation --",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Select an official designation for this coordinator"
    )
    
    class Meta:
        model = Coordinator
        fields = ['spiritual', 'name', 'designation', 'district', 'phone']
        widgets = {
            'spiritual': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter coordinator name'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit phone number'
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



#GALLERYfrom django import forms
from .models import Gallery
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

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image = cleaned_data.get('image')
        video_url = cleaned_data.get('video_url')
        video_file = cleaned_data.get('video_file')
        video_embed_code = cleaned_data.get('video_embed_code')

        if media_type == 'image':
            if not image:
                self.add_error('image', 'An image file is required when media type is Image.')

        elif media_type == 'video':
            # At least one of video_url, video_file, or video_embed_code must be provided
            if not video_url and not video_file and not video_embed_code:
                self.add_error('video_url', 'Please provide a video URL, upload a video file, or paste embed code.')
            
            # If video_url is provided, validate it
            if video_url:
                import re
                url_pattern = r'^https?://[^\s]+$'
                if not re.match(url_pattern, video_url):
                    self.add_error('video_url', 'Please enter a valid URL.')

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
            # Limit to 200MB
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
from .models import PrayerBook
from django import forms
from .models import PrayerBook

class PrayerBookForm(forms.ModelForm):
    class Meta:
        model = PrayerBook
        fields = ['title', 'image', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter prayer book title'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only JPG, JPEG, PNG, GIF, and WebP images are allowed."
                )
            # Size limit removed - no size validation
        return image

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx']
            extension = file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, Word (.doc, .docx), and Excel (.xls, .xlsx) files are allowed."
                )
            # Size limit removed - no size validation
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
            raise ValidationError('Title must be at least 5 characters long.')
        return title


class KalpanaFileForm(forms.ModelForm):
    """Form for uploading a single file with description"""
    
    class Meta:
        model = KalpanaFile
        fields = ['file', 'file_name', 'description']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.txt,.jpg,.jpeg,.png,.gif'
            }),
            'file_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display name for the file (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter description for this file...'
            }),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Validate file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('File size must be under 10MB.')
            
            # Validate file extension
            valid_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', 
                '.txt', '.jpg', '.jpeg', '.png', '.gif'
            ]
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError(
                    f'File type not supported. Allowed: {", ".join(valid_extensions)}'
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
            raise ValidationError('Title must be at least 5 characters long.')
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
            raise ValidationError('Title must be at least 5 characters long.')
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
            # Check file extension only (no size limit)
            valid_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx']
            extension = file.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file format. Please use: {', '.join(valid_extensions)}"
                )
        return file