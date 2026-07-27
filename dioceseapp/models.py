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
    Priest,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='parishes',
    limit_choices_to={'position': 'priest'},
)
    # Assistant Vicar
    assistant_vicar = models.ForeignKey(
    Priest,
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
    if not self.slug:
        base_slug = slugify(self.name)  # 👈 Use name, not first_name/last_name
        slug = base_slug
        counter = 1

        # 👈 Check Parish objects, not Priest objects
        while Parish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

    super().save(*args, **kwargs)

    def __str__(self):
        return self.name


    def get_vicar_display(self):

        if self.vicar:
            return f"{self.vicar.first_name} {self.vicar.last_name}"

        return self.vicar_name or "No vicar assigned"



  


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

    email = models.EmailField()

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
    
    designation = models.CharField(
        max_length=150,
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
    Each spiritual category can have multiple office bearers.
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