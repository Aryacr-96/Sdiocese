from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator

class Priest(models.Model):

    POSITION_CHOICES = [
        ('priest', 'Priest'),
        ('retired_priest', 'Retired Priest'),
        ('seminary_student', 'Seminary Student'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='priest'
    )

    home_parish = models.CharField(max_length=200, blank=True, null=True)

    ordained_on = models.DateField(
        blank=True,
        null=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )


    # Retirement Details
    retired_on = models.DateField(
        blank=True,
        null=True,
        verbose_name="Retired (Vicar) On"
    )

    # Pastoral Experience
    pastoral_experience = RichTextUploadingField(
    blank=True,
    null=True,
    verbose_name="Pastoral Experience"
    )
    address = models.TextField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='priests/',
        blank=True,
        null=True
    )

    description = RichTextUploadingField(
        blank=True,
        null=True
    )


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.first_name}-{self.last_name}"
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import re

class Parish(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to='parishes/', blank=True, null=True)
    location = models.CharField(max_length=250)
    map_url = models.URLField(
        "Google Maps URL",
        blank=True,
        null=True,
        help_text="Paste the Google Maps share link for this parish."
    )
    
    # ForeignKey to Priest for Vicar
    vicar = models.ForeignKey(
        'Priest',  # Use string reference to avoid circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parishes',
        limit_choices_to={'position': 'priest'},
    )
    # Assistant Vicar
    assistant_vicar = models.ForeignKey(
        'Priest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assistant_vicar_parishes',
        limit_choices_to={'position': 'priest'},
    )
    # Keep vicar_name for backward compatibility or as a fallback
    vicar_name = models.CharField(
        max_length=150, 
        blank=True, 
        null=True,
        help_text="Vicar name (used as fallback if no priest is selected)"
    )
    
    established_year = models.PositiveIntegerField()
    district = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # SOCIAL MEDIA FIELDS
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="WhatsApp number with country code (e.g., +1234567890)"
    )
    facebook_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Facebook page ID or username (e.g., parishname or 123456789)"
    )
    instagram_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Instagram username without @ (e.g., parishname)"
    )
    # Optional: Add URLs for convenience
    facebook_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Full Facebook page URL (optional, will be auto-generated if ID is provided)"
    )
    instagram_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Full Instagram profile URL (optional, will be auto-generated if ID is provided)"
    )
    
    trustee = models.CharField(max_length=150, blank=True, null=True)
    secretary = models.CharField(max_length=150, blank=True, null=True)
    number_of_families = models.PositiveIntegerField(default=0)
    description = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Parish"
        verbose_name_plural = "Parishes"

    def save(self, *args, **kwargs):
    # ALWAYS generate slug if not exists - this is the key
        if not self.slug or self.slug == '':
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Parish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

    # Auto-set vicar_name from selected vicar
        if self.vicar:
            self.vicar_name = f"{self.vicar.first_name} {self.vicar.last_name}"
        elif not self.vicar and not self.vicar_name:
            self.vicar_name = "No vicar assigned"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_vicar_display(self):
        if self.vicar:
            return f"{self.vicar.first_name} {self.vicar.last_name}"
        return self.vicar_name or "No vicar assigned"

    def get_assistant_vicar_display(self):
        if self.assistant_vicar:
            return f"{self.assistant_vicar.first_name} {self.assistant_vicar.last_name}"
        return "No assistant vicar assigned"

    # Helper methods to get social media URLs
    def get_facebook_url(self):
        """Get Facebook URL - use custom URL if set, otherwise construct from ID"""
        if self.facebook_url:
            return self.facebook_url
        if self.facebook_id:
            # Check if it's a numeric ID or username
            if self.facebook_id.isdigit():
                return f"https://www.facebook.com/profile.php?id={self.facebook_id}"
            else:
                return f"https://www.facebook.com/{self.facebook_id}"
        return None

    def get_instagram_url(self):
        """Get Instagram URL - use custom URL if set, otherwise construct from ID"""
        if self.instagram_url:
            return self.instagram_url
        if self.instagram_id:
            # Remove @ if present
            clean_id = self.instagram_id.lstrip('@')
            return f"https://www.instagram.com/{clean_id}/"
        return None

    def get_whatsapp_url(self):
        """Get WhatsApp URL for easy linking"""
        if self.whatsapp_number:
            # Remove any non-digit characters except +
            clean_number = re.sub(r'[^0-9+]', '', self.whatsapp_number)
            return f"https://wa.me/{clean_number}"
        return None

    def get_all_social_media(self):
        """Get all social media URLs as a dictionary"""
        return {
            'facebook': self.get_facebook_url(),
            'instagram': self.get_instagram_url(),
            'whatsapp': self.get_whatsapp_url(),
        }

    def has_social_media(self):
        """Check if parish has any social media links"""
        return any([
            self.facebook_url,
            self.facebook_id,
            self.instagram_url,
            self.instagram_id,
            self.whatsapp_number
        ])
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Contact(models.Model):
    full_name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    email = models.EmailField(blank=True, null=True)

    phone = models.IntegerField(
        validators=[
            MinValueValidator(1000000000),   # Minimum 10-digit number
            MaxValueValidator(9999999999),   # Maximum 10-digit number
        ]
    )

    prayer_request = models.TextField()

    is_contacted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)

            # prevent duplicate slug
            original_slug = self.slug
            counter = 1

            while Contact.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


    def __str__(self):
        return self.full_name
   # models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Phone validator
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must contain exactly 10 digits."
)

# ============================================
# OFFICE BEARER MODEL
# ============================================
class Officebearer(models.Model):
    """
    Model to store office bearer information.
    Office bearers can be linked to multiple Spiritual categories.
    """
    name = models.CharField(
        max_length=150,
        help_text="Full name of the office bearer"
    )
    designation = models.ForeignKey(
        'Designation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='officebearers',
        help_text="Designation/position of the office bearer"
    )
    
    
    image = models.ImageField(
        upload_to="officebearers/",
        blank=True,
        null=True,
        help_text="Profile photo of the office bearer"
    )
    
    phone = models.CharField(
        max_length=10,
        validators=[phone_validator],
        help_text="10-digit phone number"
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address (optional)"
    )
    
    district = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="District (optional)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when this record was last updated"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Office Bearer"
        verbose_name_plural = "Office Bearers"

    def __str__(self):
        return f"{self.name} - {self.designation}"

    def get_full_info(self):
        """Returns a string with full information about the office bearer"""
        info = f"{self.name} ({self.designation})"
        if self.phone:
            info += f" - {self.phone}"
        if self.email:
            info += f" - {self.email}"
        return info


# ============================================
# SPIRITUAL MODEL
# ============================================
class Spiritual(models.Model):
    """
    Model to store spiritual categories.
    Each spiritual category can have multiple office bearers and coordinators.
    """
    category_title = models.CharField(
        max_length=200,
        help_text="Title of the spiritual category"
    )
    
    content = RichTextUploadingField(
        blank=True,
        null=True,
        help_text="Detailed content/description of the spiritual category"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="URL-friendly version of the category title (auto-generated)"
    )
    
    # Many-to-Many relationship with Officebearer through SpiritualOfficeBearer
    officebearers = models.ManyToManyField(
        'Officebearer',
        through='SpiritualOfficeBearer',
        related_name='spiritual_categories',
        blank=True,
        help_text="Office bearers associated with this spiritual category"
    )
    
    # ✅ NEW: Many-to-Many relationship with Coordinator through SpiritualCoordinator
    coordinators = models.ManyToManyField(
        'Coordinator',
        through='SpiritualCoordinator',
        related_name='spiritual_categories',
        blank=True,
        help_text="Coordinators associated with this spiritual category"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when this record was last updated"
    )

    class Meta:
        ordering = ['category_title']
        verbose_name = "Spiritual Category"
        verbose_name_plural = "Spiritual Categories"

    def __str__(self):
        return self.category_title

    def save(self, *args, **kwargs):
        """Auto-generate slug from category_title if not provided"""
        if not self.slug:
            self.slug = slugify(self.category_title)
        super().save(*args, **kwargs)

    def get_office_bearers_count(self):
        """Returns the count of office bearers associated with this category"""
        return self.officebearers.count()

    def get_office_bearers_list(self):
        """Returns a list of all office bearers associated with this category"""
        return self.officebearers.all().order_by('name')
    
    # ✅ NEW: Helper methods for coordinators
    def get_coordinators_count(self):
        """Returns the count of coordinators associated with this category"""
        return self.coordinators.count()

    def get_coordinators_list(self):
        """Returns a list of all coordinators associated with this category"""
        return self.coordinators.all().order_by('name')


# ============================================
# SPIRITUAL OFFICE BEARER (Through Model)
# ============================================
class SpiritualOfficeBearer(models.Model):
    """
    Through model for Many-to-Many relationship between Spiritual and Officebearer.
    This allows additional fields like added_date, notes, etc.
    """
    spiritual = models.ForeignKey(
        Spiritual,
        on_delete=models.CASCADE,
        related_name='spiritual_officebearers',
        help_text="Spiritual category"
    )
    
    officebearer = models.ForeignKey(
        Officebearer,
        on_delete=models.CASCADE,
        related_name='officebearer_spirituals',
        help_text="Office bearer"
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this office bearer was added to this category"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this association is currently active"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about this association (optional)"
    )

    class Meta:
        unique_together = ['spiritual', 'officebearer']
        ordering = ['spiritual', 'officebearer']
        verbose_name = "Spiritual Office Bearer"
        verbose_name_plural = "Spiritual Office Bearers"

    def __str__(self):
        return f"{self.spiritual.category_title} - {self.officebearer.name}"

    def get_office_bearer_info(self):
        """Returns office bearer details"""
        return {
            'name': self.officebearer.name,
            'designation': self.officebearer.designation,
            'phone': self.officebearer.phone,
            'email': self.officebearer.email,
            'district': self.officebearer.district,
            'image': self.officebearer.image.url if self.officebearer.image else None,
        }


# ============================================
# SPIRITUAL COORDINATOR (Through Model) - NEW
# ============================================
class SpiritualCoordinator(models.Model):
    """
    Through model for Many-to-Many relationship between Spiritual and Coordinator.
    This allows additional fields like added_date, notes, etc.
    """
    spiritual = models.ForeignKey(
        Spiritual,
        on_delete=models.CASCADE,
        related_name='spiritual_coordinators',
        help_text="Spiritual category"
    )
    
    coordinator = models.ForeignKey(
        'Coordinator',
        on_delete=models.CASCADE,
        related_name='coordinator_spirituals',
        help_text="Coordinator"
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this coordinator was added to this category"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this association is currently active"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about this association (optional)"
    )

    class Meta:
        unique_together = ['spiritual', 'coordinator']
        ordering = ['spiritual', 'coordinator']
        verbose_name = "Spiritual Coordinator"
        verbose_name_plural = "Spiritual Coordinators"

    def __str__(self):
        return f"{self.spiritual.category_title} - {self.coordinator.name}"

    def get_coordinator_info(self):
        """Returns coordinator details"""
        return {
            'name': self.coordinator.name,
            'designation': self.coordinator.designation,
            'phone': self.coordinator.phone,
            'district': self.coordinator.district,
        }


# ============================================
# COORDINATOR MODEL - UPDATED (Removed FK to Spiritual)
# ============================================
class Coordinator(models.Model):
    """
    Model to store coordinator information.
    Coordinators can be linked to multiple Spiritual categories through ManyToMany.
    """
    name = models.CharField(
        max_length=150,
        help_text="Coordinator name"
    )
    
    # ✅ FK to Designation (Dropdown support)
    designation = models.ForeignKey(
        'Designation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinators',
        help_text="Coordinator designation/position"
    )
    
    # ✅ NEW: Added image field
    image = models.ImageField(
        upload_to="coordinators/",
        blank=True,
        null=True,
        help_text="Profile photo of the coordinator"
    )
    
    district = models.CharField(
        max_length=100,
        help_text="Coordinator district"
    )
    
    phone = models.CharField(
        max_length=10,
        validators=[phone_validator],
        help_text="10-digit phone number"
    )
    
    # ✅ NEW: Added email field
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address (optional)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when this record was last updated"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"

    def __str__(self):
        designation_name = self.designation.name if self.designation else "No Designation"
        return f"{self.name} - {designation_name}"
    
    # ✅ NEW: Helper methods
    def get_full_info(self):
        """Returns a string with full information about the coordinator"""
        info = f"{self.name}"
        if self.designation:
            info += f" ({self.designation.name})"
        if self.phone:
            info += f" - {self.phone}"
        if self.email:
            info += f" - {self.email}"
        return info
    
    def get_spiritual_categories(self):
        """Returns all spiritual categories this coordinator belongs to"""
        return self.spiritual_categories.all()
    
    def get_spiritual_categories_count(self):
        """Returns count of spiritual categories this coordinator belongs to"""
        return self.spiritual_categories.count()
    



class Designation(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="Designation name"
    )

# KARUNYA SPARSHAM

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    
from django.db import models
from django.utils.text import slugify  # <-- IMPORT HERE TOO
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Karunyasparsham(models.Model):
    # Status choices for active field
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
        ('processing', 'Processing'),
    ]
    
    # Content type choices
    CONTENT_TYPE_CHOICES = [
        ('about', 'About'),
        ('project', 'Project'),
    ]
    
    # Common fields
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='about')
    
    # About section fields
    about_title = models.CharField(max_length=200, blank=True, null=True)
    about_image = models.ImageField(upload_to='karunyasparsham/about/', blank=True, null=True)
    about_content = RichTextUploadingField(blank=True, null=True)
    
    # Project section fields
    project_title = models.CharField(max_length=200, blank=True, null=True)
    project_image = models.ImageField(upload_to='karunyasparsham/projects/', blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    project_content = RichTextUploadingField(blank=True, null=True)
    project_location = models.CharField(max_length=200, blank=True, null=True)
    
    # Project status
    active = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    
    # Foreign key to Category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='karunyasparsham_projects')
    
    # Slug field
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    
    # Additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Karunyasparsham"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['content_type']),
            models.Index(fields=['category']),
            models.Index(fields=['active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.content_type == 'about' and self.about_title:
                base_slug = slugify(self.about_title)
            elif self.content_type == 'project' and self.project_title:
                base_slug = slugify(self.project_title)
            else:
                base_slug = slugify(f"{self.content_type}-{self.id or 'temp'}")
            
            # Ensure unique slug
            self.slug = self.generate_unique_slug(base_slug)
        
        super().save(*args, **kwargs)

    def generate_unique_slug(self, base_slug):
        """Generate unique slug by adding number if slug already exists"""
        slug = base_slug
        num = 1
        while Karunyasparsham.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def __str__(self):
        if self.content_type == 'about':
            return self.about_title or "About Section"
        return self.project_title or "Project Section"

    def get_absolute_url(self):
        """Get absolute URL for the entry"""
        if self.slug:
            return reverse('karunyasparsham_detail', kwargs={'slug': self.slug})
        return reverse('karunyasparsham_detail_pk', kwargs={'pk': self.pk})

    @property
    def title(self):
        """Get title based on content type"""
        if self.content_type == 'about':
            return self.about_title
        return self.project_title

    @property
    def content(self):
        """Get content based on content type"""
        if self.content_type == 'about':
            return self.about_content
        return self.project_content

    @property
    def image(self):
        """Get image based on content type"""
        if self.content_type == 'about':
            return self.about_image
        return self.project_image


from django.db import models
from django.utils.text import slugify
import os

def publication_upload_path(instance, filename):
    return os.path.join("publications/files", filename)

def publication_image_path(instance, filename):
    return os.path.join("publications/images", filename)


class Publication(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to=publication_image_path,
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to=publication_upload_path
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Publication.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# GALLERY
from django.db import models
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class Gallery(models.Model):
    # Media type choices
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    # Common fields
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        default='image',
        verbose_name="Media Type"
    )
    
    # Image fields
    image = models.ImageField(
        upload_to='gallery/images/',
        blank=True,
        null=True,
        verbose_name="Image"
    )
    
    # Video fields
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator()],
        verbose_name="Video URL (YouTube, Vimeo, etc.)"
    )
    video_file = models.FileField(
        upload_to='gallery/videos/',
        blank=True,
        null=True,
        verbose_name="Video File"
    )
    video_embed_code = models.TextField(
        blank=True,
        null=True,
        verbose_name="Video Embed Code",
        help_text="Paste embed code from YouTube, Vimeo, or other video platforms"
    )
    
    # Common fields
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Gallery.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_media_type_display(self):
        return dict(self.MEDIA_TYPES).get(self.media_type, 'Unknown')

    def is_image(self):
        return self.media_type == 'image'

    def is_video(self):
        return self.media_type == 'video'

    def get_video_id(self):
        """Extract video ID from YouTube URL"""
        if not self.video_url:
            return None
        
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([\w-]+)',
            r'(?:youtu\.be\/)([\w-]+)',
            r'(?:youtube\.com\/embed\/)([\w-]+)',
            r'(?:youtube\.com\/shorts\/)([\w-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)
        return None

    def get_embed_url(self):
        """Get embed URL for various platforms"""
        if self.video_embed_code:
            return self.video_embed_code
        
        if not self.video_url:
            return None
        
        video_id = self.get_video_id()
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        
        if 'vimeo.com' in self.video_url:
            import re
            match = re.search(r'vimeo\.com/(\d+)', self.video_url)
            if match:
                return f'https://player.vimeo.com/video/{match.group(1)}'
        
        return self.video_url

    def get_thumbnail_url(self):
        """Get thumbnail URL for video platforms"""
        if self.is_video() and self.video_url:
            video_id = self.get_video_id()
            if video_id:
                return f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
        return None

    def clean(self):
        """Validate the model data"""
        if self.media_type == 'image' and not self.image:
            raise ValidationError({'image': 'An image is required when media type is Image.'})
        
        if self.media_type == 'video':
            if not self.video_url and not self.video_file and not self.video_embed_code:
                raise ValidationError({
                    'video_url': 'A video URL, video file, or embed code is required when media type is Video.'
                })




#PRAYER BOOKS

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


# =========================================================
# PDF FILE VALIDATOR
# =========================================================

def validate_pdf_file(value):
    """
    Validate that the uploaded file is a real PDF.

    Checks:
    1. File extension must be .pdf
    2. MIME type must be application/pdf
    3. File content must start with %PDF-
    """

    # -----------------------------------------------------
    # CHECK FILE EXTENSION
    # -----------------------------------------------------

    extension = os.path.splitext(value.name)[1].lower()

    if extension != '.pdf':
        raise ValidationError(
            "Only PDF files are allowed."
        )

    # -----------------------------------------------------
    # CHECK MIME TYPE
    # -----------------------------------------------------

    content_type = getattr(
        value,
        'content_type',
        None
    )

    if content_type and content_type != 'application/pdf':
        raise ValidationError(
            "Only PDF files are allowed."
        )

    # -----------------------------------------------------
    # CHECK ACTUAL PDF CONTENT
    # -----------------------------------------------------

    try:

        current_position = value.tell()

        value.seek(0)

        header = value.read(5)

        value.seek(current_position)

        if header != b'%PDF-':
            raise ValidationError(
                "The uploaded file is not a valid PDF."
            )

    except ValidationError:
        raise

    except Exception:

        raise ValidationError(
            "Unable to validate the uploaded PDF file."
        )


# =========================================================
# PRAYER BOOK MODEL
# =========================================================

class PrayerBook(models.Model):

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = models.CharField(
        max_length=255,
        verbose_name="Title"
    )

    # -----------------------------------------------------
    # SLUG
    # -----------------------------------------------------

    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    # -----------------------------------------------------
    # BOOK COVER IMAGE
    # -----------------------------------------------------

    image = models.ImageField(
        upload_to='prayer_books/',
        blank=True,
        null=True,
        verbose_name="Book Cover Image"
    )

    # -----------------------------------------------------
    # PDF FILE ONLY
    # -----------------------------------------------------

    file = models.FileField(
        upload_to='prayer_books/files/',
        blank=True,
        null=True,
        verbose_name="PDF File",
        validators=[
            validate_pdf_file
        ],
        help_text="Upload PDF file only"
    )

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = ['title']

        verbose_name = "Prayer Book"

        verbose_name_plural = "Prayer Books"

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    def save(self, *args, **kwargs):

        # -----------------------------------------------
        # VALIDATE PDF EVEN WHEN SAVED DIRECTLY
        # -----------------------------------------------

        if self.file:

            validate_pdf_file(
                self.file
            )

        # -----------------------------------------------
        # CREATE UNIQUE SLUG
        # -----------------------------------------------

        if not self.slug:

            base_slug = slugify(
                self.title
            )

            slug = base_slug

            counter = 1

            while PrayerBook.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        # -----------------------------------------------
        # SAVE OBJECT
        # -----------------------------------------------

        super().save(
            *args,
            **kwargs
        )

    # -----------------------------------------------------
    # STRING REPRESENTATION
    # -----------------------------------------------------

    def __str__(self):

        return self.title

    # -----------------------------------------------------
    # GET FILE EXTENSION
    # -----------------------------------------------------

    def get_file_extension(self):

        if self.file:

            return self.file.name.split(
                '.'
            )[-1].lower()

        return None

    # -----------------------------------------------------
    # GET FILE ICON
    # -----------------------------------------------------

    def get_file_icon(self):

        # Since only PDF is allowed
        return 'fa-file-pdf'




# KALPANA
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os


def validate_pdf_file(value):
    """
    Strict PDF validation.
    Checks:
    1. File extension
    2. MIME/content type
    3. PDF magic bytes
    """

    # Check extension
    ext = os.path.splitext(value.name)[1].lower()

    if ext != '.pdf':
        raise ValidationError(
            'Only PDF files are allowed.'
        )

    # Check content type if available
    content_type = getattr(value, 'content_type', None)

    if content_type and content_type != 'application/pdf':
        raise ValidationError(
            'Only PDF files are allowed.'
        )

    # Check actual PDF file signature
    try:
        current_position = value.tell()
        value.seek(0)

        file_header = value.read(5)

        value.seek(current_position)

        if file_header != b'%PDF-':
            raise ValidationError(
                'The uploaded file is not a valid PDF.'
            )

    except Exception as e:

        if isinstance(e, ValidationError):
            raise

        raise ValidationError(
            'Unable to validate the uploaded PDF file.'
        )


class Kalpana(models.Model):

    title = models.CharField(
        max_length=200,
        help_text="e.g., Kalpana 2026, Kalpana 2025"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kalpana'
        verbose_name_plural = 'Kalpana'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Kalpana.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class KalpanaFile(models.Model):

    kalpana = models.ForeignKey(
        Kalpana,
        on_delete=models.CASCADE,
        related_name='files'
    )

    file = models.FileField(
        upload_to='kalpana_files/%Y/%m/',
        validators=[
            validate_pdf_file,
            FileExtensionValidator(['pdf'])
        ],
        help_text="Upload PDF file only"
    )

    file_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Display name for the file"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of this file"
    )

    file_type = models.CharField(
        max_length=20,
        blank=True
    )

    file_size = models.CharField(
        max_length=20,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Kalpana File'
        verbose_name_plural = 'Kalpana Files'

    def __str__(self):
        return self.file_name or self.file.name

    def save(self, *args, **kwargs):

        # Validate the file even when saved outside the form
        if self.file:
            validate_pdf_file(self.file)

        # Automatically set file name
        if not self.file_name and self.file:
            self.file_name = os.path.basename(
                self.file.name
            )

        # Automatically determine file type
        if self.file:

            self.file_type = 'pdf'

        # Automatically calculate file size
        if (
            not self.file_size
            and self.file
            and hasattr(self.file, 'size')
        ):

            size = self.file.size

            if size < 1024:

                self.file_size = f"{size} B"

            elif size < 1024 * 1024:

                self.file_size = (
                    f"{size / 1024:.1f} KB"
                )

            else:

                self.file_size = (
                    f"{size / (1024 * 1024):.2f} MB"
                )

        super().save(*args, **kwargs)


# EVENTS


from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    description = models.TextField()
    event_date = models.DateField()  # Changed to DateField for date only
    event_time = models.TimeField()  # New separate time field
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_event_datetime(self):
        """Combine date and time into a single datetime object"""
        return timezone.datetime.combine(self.event_date, self.event_time)

    class Meta:
        ordering = ['event_date', 'event_time']


#DOWNLOADS

from django.db import models
from django.core.validators import FileExtensionValidator

class Download(models.Model):
    """
    Simple model for downloadable documents.
    """
    
    DOCUMENT_TYPES = [
        ('church_account_manual', 'Church Account Manual'),
        ('constitution_1934', '1934 Constitution'),
        ('guidelines', 'Guidelines'),
    ]
    
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        verbose_name="Document Type"
    )
    
    file = models.FileField(
        upload_to='downloads/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'xls', 'xlsx'])],
        help_text="Upload PDF, Word, or Excel files"
    )

    class Meta:
        db_table = 'downloads'
        ordering = ['document_type']
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'

    def __str__(self):
        return f"{self.get_document_type_display()}"





# SYNOD

from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Synod(models.Model):

    name = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to='synod/',
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    content = RichTextUploadingField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    phone_numbers = models.JSONField(
        default=list,
        blank=True,
        help_text='Enter multiple phone numbers as a JSON list.'
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    facebook = models.URLField(
        blank=True,
        null=True
    )

    instagram = models.URLField(
        blank=True,
        null=True
    )

    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        new_slug = slugify(self.name)

        base_slug = new_slug
        counter = 1

        while Synod.objects.filter(
            slug=new_slug
        ).exclude(
            pk=self.pk
        ).exists():

            new_slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = new_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Synod"
        verbose_name_plural = "Synods"
        ordering = ['name']