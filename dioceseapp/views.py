from django.urls import path
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

# ADD THESE IMPORTS:
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from .forms import CategoryForm, OfficebearerForm, SpiritualForm, adminform 
from .forms import (SpiritualForm,
    OfficebearerFormSet
)

def index(request):
    return render(request,'index.html')
# ABOUT CHURCH
def believe(request):
    return render(request,'about/believe.html')
def catholicate(request):
    return render(request,'about/catholicate.html')
def history(request):
    return render(request,'about/history.html')
def malankara(request):
    return render(request,'about/malankara.html')



from django.shortcuts import render, get_object_or_404
from .models import Synod


def synod(request):
    synods = Synod.objects.all()

    return render(
        request,
        'about/synod.html',
        {
            'synods': synods
        }
    )


def synod_detail(request, slug):
    synod = get_object_or_404(
        Synod,
        slug=slug
    )

    return render(
        request,
        'about/synod_detail.html',
        {
            'synod': synod
        }
    )
def throne(request):
    return render(request,'about/throne.html')


# ABOUT DIOCESE

def batherydiocese(request):
    return render(request,'diocese/batherydiocese.html')
def committe(request):
    return render(request,'diocese/committe.html')
def council(request):
    return render(request,'diocese/council.html')
def diocesehistory(request):
    return render(request,'diocese/diocesehistory.html')
def metropolitans(request):
    return render(request, 'diocese/metropolitans.html')
def priest(request):

    priests = Priest.objects.filter(
        position='priest'
    ).order_by('first_name')

    retired_priests = Priest.objects.filter(
        position='retired_priest'
    ).order_by('first_name')

    students = Priest.objects.filter(
        position='seminary_student'
    ).order_by('first_name')

    return render(
        request,
        'diocese/priest.html',
        {
            'priests': priests,
            'retired_priests': retired_priests,
            'students': students,
        }
    )

def priest_details(request, slug):

    priest = get_object_or_404(
        Priest,
        slug=slug
    )

    return render(
        request,
        'diocese/priest_details.html',
        {
            'priest': priest
        }
    )
def priestretired_details(request, slug):

    priest = get_object_or_404(
        Priest,
        slug=slug,
        position='retired_priest'
    )

    return render(
        request,
        'diocese/priestretired_detail.html',
        {
            'priest': priest
        }
    )
def parish(request):
    parishes = Parish.objects.all().order_by('name')

    return render(request, 'diocese/parish.html', {
        'parishes': parishes,
    })


def parish_details(request, slug):
    parish = get_object_or_404(Parish, slug=slug)
    return render(request, 'diocese/parish_details.html', {
        'parish': parish,
    })

# Add ID-based fallback view
def parish_details_by_id(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)
    return render(request, 'diocese/parish_details.html', {
        'parish': parish,
    })





################## SYNOD DETAIL #################


















































# SRIRITUAL ORGANIZATIONS

def vaidika(request):
    return render(request,'spiritual/vidhika.html')
def sundayschool(request):
    return render(request,'spiritual/sunday.html')
def vanitha(request):
    return render(request,'spiritual/vanitha.html')
def prarthana(request):
    return render(request,'spiritual/prarthayogam.html')
def mgocsm(request):
    return render(request,'spiritual/mgocsm.html')
def baskiyoma(request):
    return render(request,'spiritual/baskiyoma.html')
def ocym(request):
    return render(request,'spiritual/ocym.html')
def sushrushaka(request):
    return render(request,'spiritual/sushrushaka.html')
def balika(request):
    return render(request,'spiritual/balika.html')
def human(request):
    return render(request,'spiritual/human.html')
def divya(request):
    return render(request,'spiritual/divya.html')
def suvishesham(request):
    return render(request,'spiritual/suvishesham.html')
def sdof(request):
    return render(request,'spiritual/sdof.html')
def sjof(request):
    return render(request,'spiritual/sjof.html')



# KARUNYA SPARSAM

def karunyam(request):
    about = Karunyasparsham.objects.filter(content_type='about').first()
    projects = Karunyasparsham.objects.filter(content_type='project')

    context = {
        'about': about,
        'projects': projects,
    }
    return render(request, 'karunyam/karunyam.html', context)
from .models import Karunyasparsham

def projects(request):
    projects = Karunyasparsham.objects.filter(content_type='project')

    return render(request, 'karunyam/projects.html', {
        'projects': projects,
    })
from django.shortcuts import get_object_or_404

def projects_detail(request, slug):
    project = get_object_or_404(
        Karunyasparsham,
        slug=slug,
        content_type='project'
    )

    return render(request, 'karunyam/projectsdetail.html', {
        'project': project,
    })



# INSTITUTIONS


def school(request):
    return render(request,'institutions/school.html')
def school_detail(request):
    return render(request,'institutions/schooldetail.html')
def college(request):
    return render(request,'institutions/college.html')
def college_detail(request):
    return render(request,'institutions/collegedetail.html')
def retreat(request):
    return render(request,'institutions/retreat.html')
def retreat_detail(request):
    return render(request,'institutions/retreatdetail.html')


# MEDIA

from django.shortcuts import render
from dioceseapp.models import Publication

def publications(request):
    # Get all publications ordered by upload date (newest first)
    publications = Publication.objects.all().order_by('-uploaded_at')
    
    return render(request, 'media/publications.html', {
        'publications': publications,
        'total_publications': publications.count(),
    })





def images(request):
    """Public gallery view showing only images"""
    # Get only image type gallery items
    items = Gallery.objects.filter(media_type='image').order_by('-created_at')
    
    # Pagination - 12 items per page
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'total_items': items.count(),
    }
    return render(request, 'media/images.html', context)

def videos(request):
    """Public video gallery view showing only videos"""
    # Get only video type gallery items
    items = Gallery.objects.filter(media_type='video').order_by('-created_at')
    
    # Pagination - 9 items per page
    paginator = Paginator(items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'total_items': items.count(),
    }
    return render(request, 'media/videos.html', context)
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Event
import calendar as cal_module


def calendar(request):
    now = timezone.now()
    year = request.GET.get('year', now.year)
    month = request.GET.get('month', now.month)
    
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year = now.year
        month = now.month
    
    # Get all events for this month
    events = Event.objects.filter(
        event_date__year=year,
        event_date__month=month
    ).order_by('event_date', 'event_time')
    
    # Create events dictionary for JavaScript with full event details
    events_dict = {}
    for event in events:
        date_key = event.event_date.strftime('%Y-%m-%d')
        event_data = {
            'title': event.title,
            'time': event.event_time.strftime('%I:%M %p'),
            'location': event.location,
            'id': event.id,
            'description': event.description[:100] if event.description else '',
        }
        if date_key in events_dict:
            events_dict[date_key].append(event_data)
        else:
            events_dict[date_key] = [event_data]
    
    # Calendar data
    cal = cal_module.monthcalendar(year, month)
    month_name = cal_module.month_name[month]
    month_names = list(cal_module.month_name)[1:]
    year_range = range(2000, 2031)
    
    context = {
        'calendar': cal,
        'month': month,
        'year': year,
        'month_name': month_name,
        'month_names': month_names,
        'year_range': year_range,
        'events_dict': events_dict,
        'events_count': events.count(),
        'now': now,
    }
    return render(request, 'media/calendar.html', context)

# Public: Event detail (using ID)

def events(request):
    now = timezone.now()
    events = Event.objects.filter(
        Q(event_date__gt=now.date()) | 
        (Q(event_date=now.date()) & Q(event_time__gt=now.time()))
    ).order_by('event_date', 'event_time')
    
    # Get all events for counting
    total_events = Event.objects.count()
    upcoming_count = events.count()
    
    context = {
        'events': events,
        'total_events': total_events,
        'upcoming_count': upcoming_count,
        'now': now,
    }
    return render(request, 'media/events.html', context)


# DOWNLOADS

def kalpana(request):
    """Display all Kalpana entries"""
    kalpanas = Kalpana.objects.all().order_by('-created_at')
    return render(request, 'downloads/kalpana.html', {
        'kalpanas': kalpanas
    })

def kalpanadetail(request, slug):
    """Display details of a specific Kalpana"""
    kalpana = get_object_or_404(Kalpana, slug=slug)
    files = kalpana.files.all().order_by('-uploaded_at')
    return render(request, 'downloads/kalpanadetail.html', {
        'kalpana': kalpana,
        'files': files
    })

import mimetypes

from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect

from .models import KalpanaFile


def kalpana_view_file(request, file_id):
    file_obj = get_object_or_404(KalpanaFile, id=file_id)

    if not file_obj.file:
        return redirect(
            'kalpanadetail',
            slug=file_obj.kalpana.slug
        )

    # Detect the actual file type
    content_type, _ = mimetypes.guess_type(file_obj.file.name)

    if not content_type:
        content_type = 'application/octet-stream'

    response = FileResponse(
        file_obj.file.open('rb'),
        content_type=content_type
    )

    # Tell browser to OPEN instead of download
    response['Content-Disposition'] = (
        f'inline; filename="{file_obj.file.name.split("/")[-1]}"'
    )

    return response

def downloads(request):
    all_downloads = Download.objects.all()

    church_account_manual = Download.objects.filter(
        document_type='church_account_manual'
    ).first()

    constitution_1934 = Download.objects.filter(
        document_type='constitution_1934'
    ).first()

    guidelines = Download.objects.filter(
        document_type='guidelines'
    ).first()

    context = {
        'downloads': all_downloads,
        'church_account_manual': church_account_manual,
        'constitution_1934': constitution_1934,
        'guidelines': guidelines,
        'page_title': 'Downloads',
        'additional_info': 'Download our resources and documents',
    }

    return render(request, 'media/downloads.html', context)


def prayerbook(request):
    """Public view for prayer books"""
    books = PrayerBook.objects.all().order_by('title')
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'total_books': books.count(),
    }
    return render(request, 'downloads/prayerbooks.html', context)


# CONTACT


def contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your prayer request has been submitted successfully."
            )

            return redirect('contact')

    else:
        form = ContactForm()

    return render(
        request,
        'contact.html',
        {
            'form': form
        }
    )




# ================= ADMIN =================
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from .models import Officebearer, Priest,Parish, Spiritual
from .forms import PriestForm,ParishForm


@never_cache
def admin(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == "POST":
        form = adminform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('admin')
    else:
        form = adminform()

    return render(request, 'admin/adminlogin.html', {'form': form})


@never_cache
def admin_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'admin/dashboard.html')
    return redirect('admin')


@never_cache
def logoutadmin(request):
    logout(request)
    return redirect('admin')



# ================= PRIEST ADMIN =================from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .models import Priest
from .forms import PriestForm


# Priest List
@never_cache
def priests(request):
    if not request.user.is_authenticated:
        return redirect('admin')

    priests = Priest.objects.all().order_by('first_name')

    return render(request, 'admin/priest/priests.html', {
        'priests': priests,
    })


# Add Priest
@never_cache
def add_priest(request):
    if not request.user.is_authenticated:
        return redirect('admin')
    
    if request.method == 'POST':
        form = PriestForm(request.POST, request.FILES)
        if form.is_valid():
            priest = form.save()
            messages.success(request, f'Priest "{priest.first_name} {priest.last_name}" added successfully!')
            return redirect('admin_priests')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # Debug: Print errors to console
    else:
        form = PriestForm()
    
    return render(request, 'admin/priest/addpriest.html', {'form': form})


# Edit Priest
@never_cache
def edit_priest(request, priest_id):
    if not request.user.is_authenticated:
        return redirect('admin')

    priest = get_object_or_404(Priest, pk=priest_id)

    if request.method == 'POST':
        form = PriestForm(
            request.POST,
            request.FILES,
            instance=priest
        )

        if form.is_valid():
            form.save()
            messages.success(request, f'Priest "{priest.first_name} {priest.last_name}" updated successfully!')
            return redirect('admin_priests')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)
    else:
        form = PriestForm(instance=priest)

    return render(request, 'admin/priest/editpriest.html', {
        'form': form,
        'priest': priest,
    })


# Delete Priest
@never_cache
def delete_priest(request, priest_id):
    if not request.user.is_authenticated:
        return redirect('admin')

    priest = get_object_or_404(Priest, pk=priest_id)

    if request.method == 'POST':
        priest_name = f"{priest.first_name} {priest.last_name}"
        priest.delete()
        messages.success(request, f'Priest "{priest_name}" deleted successfully!')
        return redirect('admin_priests')

    return render(request, 'admin/priest/deletepriest.html', {
        'priest': priest,
    })


# View Priest
@never_cache
def view_priest(request, priest_id):
    if not request.user.is_authenticated:
        return redirect('admin')

    priest = get_object_or_404(Priest, pk=priest_id)

    return render(request, 'admin/priest/viewpriest.html', {
        'priest': priest,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import ParishForm
from .models import Parish
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
# PARISH ADMIN
@never_cache
def parishes(request):
    if not request.user.is_authenticated:
        return redirect('admin')

    parishes = Parish.objects.all()

    return render(request, 'admin/parish/parish.html', {
        'parishes': parishes,
    })

# ADD PARISH
@never_cache
def add_parish(request):

    if not request.user.is_authenticated:
        return redirect('admin')
    if request.method == 'POST':
        form = ParishForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            parish = form.save(commit=False)
            # Save vicar name automatically
            if parish.vicar:
                parish.vicar_name = (
                    f"{parish.vicar.first_name} "
                    f"{parish.vicar.last_name}"
                )
            # Clean Google Maps URL
            if parish.map_url:
                parish.map_url = clean_google_maps_url(
                    parish.map_url
                )
            
            # NEW: Clean social media fields
            if parish.whatsapp_number:
                parish.whatsapp_number = clean_whatsapp_number(parish.whatsapp_number)
            
            if parish.instagram_id:
                parish.instagram_id = clean_instagram_id(parish.instagram_id)
            
            if parish.facebook_id:
                parish.facebook_id = clean_facebook_id(parish.facebook_id)
            
            parish.save()
            messages.success(
                request,
                f'Parish "{parish.name}" added successfully!'
            )
            return redirect('admin_parishes')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ParishForm()
    return render(
        request,
        'admin/parish/addparish.html',
        {
            'form': form
        }
    )

# EDIT PARISH
def edit_parish(request, parish_id):
    parish = get_object_or_404(Parish, id=parish_id)

    # Exclude current vicar from assistant list
    assistant_vicars = Priest.objects.exclude(id=parish.vicar.id if parish.vicar else None)

    if request.method == "POST":
        form = ParishForm(request.POST, request.FILES, instance=parish)

        if form.is_valid():
            parish = form.save(commit=False)

            # Save assistant vicar manually
            assistant_vicar_id = request.POST.get('assistant_vicar')

            if assistant_vicar_id:
                parish.assistant_vicar_id = assistant_vicar_id
            else:
                parish.assistant_vicar = None

            # NEW: Clean social media fields before saving
            if parish.whatsapp_number:
                parish.whatsapp_number = clean_whatsapp_number(parish.whatsapp_number)
            
            if parish.instagram_id:
                parish.instagram_id = clean_instagram_id(parish.instagram_id)
            
            if parish.facebook_id:
                parish.facebook_id = clean_facebook_id(parish.facebook_id)

            parish.save()

            messages.success(
                request,
                f'Parish "{parish.name}" updated successfully!'
            )
            return redirect('admin_parishes')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:
        form = ParishForm(instance=parish)

    context = {
        'form': form,
        'parish': parish,
        'assistant_vicars': assistant_vicars,
    }

    return render(request, 'admin/parish/editparish.html', context)

# DELETE PARISH
@never_cache
def delete_parish(request, parish_id):
    if not request.user.is_authenticated:
        return redirect('admin')

    parish = get_object_or_404(Parish, id=parish_id)

    if request.method == 'POST':
        parish_name = parish.name
        parish.delete()
        messages.success(request, f'Parish "{parish_name}" deleted successfully!')
        return redirect('admin_parishes')

    return render(request, 'admin/parish/deleteparish.html', {
        'parish': parish
    })

# VIEW PARISH
@never_cache
def view_parish(request, parish_id):
    if not request.user.is_authenticated:
        return redirect('admin')

    parish = get_object_or_404(Parish, id=parish_id)
    
    # Generate proper embed URL
    embed_url = None
    if parish.map_url:
        embed_url = get_google_maps_embed_url(parish.map_url, parish.location)

    # NEW: Get social media URLs
    social_media = {
        'facebook': parish.get_facebook_url(),
        'instagram': parish.get_instagram_url(),
        'whatsapp': parish.get_whatsapp_url(),
    }

    return render(request, 'admin/parish/viewparish.html', {
        'parish': parish,
        'embed_url': embed_url,
        'social_media': social_media,  # NEW
    })

# Helper Functions for Google Maps
def clean_google_maps_url(url):
    """
    Clean and standardize Google Maps URLs
    """
    if not url:
        return url
    
    # Remove whitespace
    url = url.strip()
    
    # Handle different Google Maps URL formats
    # Format 1: https://www.google.com/maps/place/...
    # Format 2: https://www.google.com/maps/@lat,lng,zoom
    # Format 3: https://maps.app.goo.gl/... (short URL)
    
    return url

def get_google_maps_embed_url(url, location=None):
    """
    Generate a proper Google Maps embed URL
    """
    if not url:
        return None
    
    # If it's a short URL (goo.gl), we can't directly embed it
    if 'maps.app.goo.gl' in url:
        # Use location as fallback for embedding
        if location:
            return f"https://www.google.com/maps/embed/v1/place?q={location.replace(' ', '+')}&key=YOUR_GOOGLE_MAPS_API_KEY"
        return None
    
    # Extract place name from URL
    # Example: https://www.google.com/maps/place/St+Mary's+Church/@lat,lng,zoom
    if '/place/' in url:
        # Extract the place name
        match = re.search(r'/place/([^/@]+)', url)
        if match:
            place_name = match.group(1).replace('+', ' ')
            return f"https://www.google.com/maps/embed/v1/place?q={place_name.replace(' ', '+')}&key=YOUR_GOOGLE_MAPS_API_KEY"
    
    # If we have location, use it
    if location:
        return f"https://www.google.com/maps/embed/v1/place?q={location.replace(' ', '+')}&key=YOUR_GOOGLE_MAPS_API_KEY"
    
    # Fallback: return the original URL (will open in new tab)
    return url

def get_map_preview_url(parish):
    """
    Generate a static map preview URL
    """
    if not parish.map_url:
        return None
    
    # Try to extract coordinates
    coord_match = re.search(r'/@([-\d.]+),([-\d.]+)', parish.map_url)
    if coord_match:
        lat, lng = coord_match.groups()
        return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=15&size=600x300&markers=color:red|{lat},{lng}&key=YOUR_GOOGLE_MAPS_API_KEY"
    
    # Use location for geocoding (requires API key)
    if parish.location:
        return f"https://maps.googleapis.com/maps/api/staticmap?center={parish.location.replace(' ', '+')}&zoom=14&size=600x300&key=YOUR_GOOGLE_MAPS_API_KEY"
    
    return None

# NEW: Helper Functions for Social Media Cleaning
def clean_whatsapp_number(number):
    """
    Clean WhatsApp number: remove spaces and special characters, ensure + prefix
    """
    if not number:
        return number
    
    # Remove spaces and special characters except +
    cleaned = re.sub(r'[^0-9+]', '', number.strip())
    
    # Ensure it starts with +
    if cleaned and not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    return cleaned

def clean_instagram_id(username):
    """
    Clean Instagram username: remove @ and whitespace
    """
    if not username:
        return username
    
    # Remove @ if present and strip whitespace
    cleaned = username.strip().lstrip('@')
    
    # Remove trailing slashes
    cleaned = cleaned.rstrip('/')
    
    return cleaned

def clean_facebook_id(facebook_id):
    """
    Clean Facebook ID: extract from URL if full URL provided, remove slashes
    """
    if not facebook_id:
        return facebook_id
    
    facebook_id = facebook_id.strip()
    
    # If it's a full URL, extract the ID/username
    if 'facebook.com' in facebook_id:
        # Try to extract from various Facebook URL formats
        patterns = [
            r'facebook\.com/(?:profile\.php\?id=)?([^/?&]+)',
            r'fb\.com/([^/?&]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, facebook_id)
            if match:
                return match.group(1)
        
        # If no pattern matches, return as is
        return facebook_id
    
    # Remove trailing slashes
    facebook_id = facebook_id.rstrip('/')
    
    return facebook_id



from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm


# Contact List
from django.contrib import messages

def contactpage(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your prayer request has been submitted successfully."
            )
            return redirect('contactpage')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    
    contacts = Contact.objects.all().order_by('-created_at')
    context = {
        'form': form,
        'contacts': contacts
    }
    return render(request, 'admin/contact/contact.html', context)


# Contact Detail
def contactview(request, id):
    contact = get_object_or_404(Contact, id=id)
    context = {
        'contact': contact
    }
    return render(request, 'admin/contact/contactview.html', context)


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def contactdelete(request, id):
    contact = get_object_or_404(Contact, id=id)
    
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Prayer request deleted successfully.")
        return redirect('contactpage')
    
    # If it's a GET request, redirect to the contact page with an error
    messages.error(request, "Invalid request method.")
    return redirect('contactpage')

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Spiritual, Officebearer, SpiritualOfficeBearer, Coordinator, SpiritualCoordinator, Designation
from .forms import (
    SpiritualForm, 
    OfficebearerForm, 
    CoordinatorForm,
    NewOfficeBearerForm,
    NewCoordinatorForm,
    SpiritualOfficeBearerFormSet,
    SpiritualCoordinatorFormSet,
    DesignationForm
)

# ============================================
# SPIRITUAL VIEWS
# ============================================

def spiritual_list(request):
    """Display list of all spiritual categories"""
    spirituals = Spiritual.objects.all().order_by('-created_at')
    total_bearers = SpiritualOfficeBearer.objects.count()
    total_coordinators = SpiritualCoordinator.objects.count()
    
    return render(request, 'admin/spiritual/spiritual.html', {
        'spirituals': spirituals,
        'total_bearers': total_bearers,
        'total_coordinators': total_coordinators
    })

def spiritual_detail(request, id):
    """Display details of a specific spiritual category"""
    spiritual = get_object_or_404(Spiritual, id=id)
    officebearers = spiritual.officebearers.all()
    coordinators = spiritual.coordinators.all()
    
    return render(request, 'admin/spiritual/spiritual_detail.html', {
        'spiritual': spiritual,
        'officebearers': officebearers,
        'coordinators': coordinators
    })
# views.py - Complete with all imports

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import (
    Spiritual, 
    Officebearer, 
    SpiritualOfficeBearer, 
    Coordinator, 
    SpiritualCoordinator, 
    Designation
)
from .forms import (
    SpiritualForm, 
    OfficebearerForm, 
    CoordinatorForm,
    NewOfficeBearerForm,
    NewCoordinatorForm,
    SpiritualOfficeBearerFormSet,
    SpiritualCoordinatorFormSet,
    DesignationForm
)


# ============================================
# SPIRITUAL VIEWS
# ============================================

def add_spiritual(request):
    if request.method == "POST":
        form = SpiritualForm(request.POST, request.FILES)
        
        if form.is_valid():
            spiritual = form.save()
            
            # Handle selected existing office bearers
            selected_bearers = request.POST.getlist('selected_bearers')
            for ob_id in selected_bearers:
                if ob_id:
                    try:
                        officebearer = Officebearer.objects.get(id=ob_id)
                        SpiritualOfficeBearer.objects.create(
                            spiritual=spiritual,
                            officebearer=officebearer
                        )
                    except Officebearer.DoesNotExist:
                        pass
            
            # Handle selected existing coordinators
            selected_coordinators = request.POST.getlist('selected_coordinators')
            for coord_id in selected_coordinators:
                if coord_id:
                    try:
                        coordinator = Coordinator.objects.get(id=coord_id)
                        SpiritualCoordinator.objects.create(
                            spiritual=spiritual,
                            coordinator=coordinator
                        )
                    except Coordinator.DoesNotExist:
                        pass
            
            # Handle new office bearers with images
            new_names = request.POST.getlist('new_officebearer_name[]')
            new_designations = request.POST.getlist('new_officebearer_designation[]')
            new_phones = request.POST.getlist('new_officebearer_phone[]')
            new_emails = request.POST.getlist('new_officebearer_email[]')
            new_districts = request.POST.getlist('new_officebearer_district[]')
            new_images = request.FILES.getlist('new_officebearer_image[]')
            
            for i in range(len(new_names)):
                name = new_names[i].strip()
                if name:
                    designation_id = new_designations[i] if i < len(new_designations) else None
                    designation = None
                    if designation_id:
                        try:
                            designation = Designation.objects.get(id=designation_id)
                        except Designation.DoesNotExist:
                            messages.warning(request, f"Designation not found for {name}")
                    
                    officebearer = Officebearer(
                        name=name,
                        designation=designation,
                        phone=new_phones[i].strip() if i < len(new_phones) else '',
                        email=new_emails[i].strip() if i < len(new_emails) else '',
                        district=new_districts[i].strip() if i < len(new_districts) else '',
                    )
                    
                    if i < len(new_images) and new_images[i]:
                        officebearer.image = new_images[i]
                    
                    officebearer.save()
                    
                    SpiritualOfficeBearer.objects.create(
                        spiritual=spiritual,
                        officebearer=officebearer
                    )
            
            # Handle new coordinators
            new_coord_names = request.POST.getlist('new_coordinator_name[]')
            new_coord_designations = request.POST.getlist('new_coordinator_designation[]')
            new_coord_districts = request.POST.getlist('new_coordinator_district[]')
            new_coord_phones = request.POST.getlist('new_coordinator_phone[]')
            new_coord_emails = request.POST.getlist('new_coordinator_email[]')
            new_coord_images = request.FILES.getlist('new_coordinator_image[]')
            
            for i in range(len(new_coord_names)):
                name = new_coord_names[i].strip()
                if name:
                    designation_id = new_coord_designations[i] if i < len(new_coord_designations) else None
                    designation = None
                    if designation_id:
                        try:
                            designation = Designation.objects.get(id=designation_id)
                        except Designation.DoesNotExist:
                            messages.warning(request, f"Designation not found for {name}")
                    
                    coordinator = Coordinator(
                        name=name,
                        designation=designation,
                        district=new_coord_districts[i].strip() if i < len(new_coord_districts) else '',
                        phone=new_coord_phones[i].strip() if i < len(new_coord_phones) else '',
                        email=new_coord_emails[i].strip() if i < len(new_coord_emails) else '',
                    )
                    
                    if i < len(new_coord_images) and new_coord_images[i]:
                        coordinator.image = new_coord_images[i]
                    
                    coordinator.save()
                    
                    SpiritualCoordinator.objects.create(
                        spiritual=spiritual,
                        coordinator=coordinator
                    )
            
            messages.success(request, "Spiritual category added successfully!")
            return redirect('spiritual')
        else:
            messages.error(request, "Please correct the errors below.")
            # Debug: Print form errors to console
            print("Form errors:", form.errors)
    else:
        form = SpiritualForm()
    
    existing_bearers = Officebearer.objects.select_related('designation').all().order_by('name')
    existing_coordinators = Coordinator.objects.select_related('designation').all().order_by('name')
    designations = Designation.objects.all().order_by('name')
    
    return render(request, 'admin/spiritual/addspiritual.html', {
        'form': form,
        'existing_bearers': existing_bearers,
        'existing_coordinators': existing_coordinators,
        'selected_bearers': [],
        'selected_coordinators': [],
        'designations': designations,
        'editing': False
    })
def edit_spiritual(request, id):
    spiritual = get_object_or_404(Spiritual, id=id)
    
    if request.method == "POST":
        form = SpiritualForm(request.POST, request.FILES, instance=spiritual)
        
        if form.is_valid():
            spiritual = form.save()
            
            # Clear existing associations
            SpiritualOfficeBearer.objects.filter(spiritual=spiritual).delete()
            SpiritualCoordinator.objects.filter(spiritual=spiritual).delete()
            
            # Handle selected existing office bearers
            selected_bearers = request.POST.getlist('selected_bearers')
            for ob_id in selected_bearers:
                if ob_id:
                    try:
                        officebearer = Officebearer.objects.get(id=ob_id)
                        SpiritualOfficeBearer.objects.create(
                            spiritual=spiritual,
                            officebearer=officebearer
                        )
                    except Officebearer.DoesNotExist:
                        pass
            
            # Handle selected existing coordinators
            selected_coordinators = request.POST.getlist('selected_coordinators')
            for coord_id in selected_coordinators:
                if coord_id:
                    try:
                        coordinator = Coordinator.objects.get(id=coord_id)
                        SpiritualCoordinator.objects.create(
                            spiritual=spiritual,
                            coordinator=coordinator
                        )
                    except Coordinator.DoesNotExist:
                        pass
            
            # Handle new office bearers
            new_names = request.POST.getlist('new_officebearer_name[]')
            new_designations = request.POST.getlist('new_officebearer_designation[]')
            new_phones = request.POST.getlist('new_officebearer_phone[]')
            new_emails = request.POST.getlist('new_officebearer_email[]')
            new_districts = request.POST.getlist('new_officebearer_district[]')
            new_images = request.FILES.getlist('new_officebearer_image[]')
            
            for i in range(len(new_names)):
                name = new_names[i].strip()
                if name:
                    designation_id = new_designations[i] if i < len(new_designations) else None
                    designation = None
                    if designation_id:
                        try:
                            designation = Designation.objects.get(id=designation_id)
                        except Designation.DoesNotExist:
                            pass
                    
                    officebearer = Officebearer(
                        name=name,
                        designation=designation,
                        phone=new_phones[i].strip() if i < len(new_phones) else '',
                        email=new_emails[i].strip() if i < len(new_emails) else '',
                        district=new_districts[i].strip() if i < len(new_districts) else '',
                    )
                    
                    if i < len(new_images) and new_images[i]:
                        officebearer.image = new_images[i]
                    
                    officebearer.save()
                    
                    SpiritualOfficeBearer.objects.create(
                        spiritual=spiritual,
                        officebearer=officebearer
                    )
            
            # Handle new coordinators
            new_coord_names = request.POST.getlist('new_coordinator_name[]')
            new_coord_designations = request.POST.getlist('new_coordinator_designation[]')
            new_coord_districts = request.POST.getlist('new_coordinator_district[]')
            new_coord_phones = request.POST.getlist('new_coordinator_phone[]')
            new_coord_emails = request.POST.getlist('new_coordinator_email[]')
            new_coord_images = request.FILES.getlist('new_coordinator_image[]')
            
            for i in range(len(new_coord_names)):
                name = new_coord_names[i].strip()
                if name:
                    designation_id = new_coord_designations[i] if i < len(new_coord_designations) else None
                    designation = None
                    if designation_id:
                        try:
                            designation = Designation.objects.get(id=designation_id)
                        except Designation.DoesNotExist:
                            pass
                    
                    coordinator = Coordinator(
                        name=name,
                        designation=designation,
                        district=new_coord_districts[i].strip() if i < len(new_coord_districts) else '',
                        phone=new_coord_phones[i].strip() if i < len(new_coord_phones) else '',
                        email=new_coord_emails[i].strip() if i < len(new_coord_emails) else '',
                    )
                    
                    if i < len(new_coord_images) and new_coord_images[i]:
                        coordinator.image = new_coord_images[i]
                    
                    coordinator.save()
                    
                    SpiritualCoordinator.objects.create(
                        spiritual=spiritual,
                        coordinator=coordinator
                    )
            
            messages.success(request, "Spiritual category updated successfully!")
            return redirect('spiritual')
        else:
            messages.error(request, "Please correct the errors below.")
            print("Form errors:", form.errors)
    else:
        form = SpiritualForm(instance=spiritual)
    
    # ===== GET ALL DATA FOR TEMPLATE =====
    # Get all office bearers
    existing_bearers = Officebearer.objects.select_related('designation').all().order_by('name')
    
    # Get all coordinators
    existing_coordinators = Coordinator.objects.select_related('designation').all().order_by('name')
    
    # Get selected office bearer IDs for this spiritual
    selected_bearers = SpiritualOfficeBearer.objects.filter(
        spiritual=spiritual
    ).values_list('officebearer_id', flat=True)
    
    # Get selected coordinator IDs for this spiritual
    selected_coordinators = SpiritualCoordinator.objects.filter(
        spiritual=spiritual
    ).values_list('coordinator_id', flat=True)
    
    # Get all designations for dropdowns
    designations = Designation.objects.all().order_by('name')
    
    # Debug prints
    print(f"Spiritual ID: {spiritual.id}")
    print(f"Selected Bearers: {list(selected_bearers)}")
    print(f"Selected Coordinators: {list(selected_coordinators)}")
    
    return render(request, 'admin/spiritual/editspiritual.html', {
        'form': form,
        'spiritual': spiritual,
        'existing_bearers': existing_bearers,
        'existing_coordinators': existing_coordinators,
        'selected_bearers': list(selected_bearers),
        'selected_coordinators': list(selected_coordinators),
        'designations': designations,
        'editing': True,
    })

def view_spiritual(request, id):
    """View Spiritual Category"""
    spiritual = get_object_or_404(
        Spiritual.objects.prefetch_related(
            'officebearers',
            'coordinators'
        ),
        id=id
    )

    officebearers = spiritual.officebearers.select_related('designation').all()
    coordinators = spiritual.coordinators.select_related('designation').all()

    return render(
        request,
        'admin/spiritual/viewspiritual.html',
        {
            'spiritual': spiritual,
            'officebearers': officebearers,
            'coordinators': coordinators,
        }
    )

def delete_spiritual(request, id):
    """Delete a spiritual category"""
    spiritual = get_object_or_404(Spiritual, id=id)
    
    if request.method == "POST":
        category_title = spiritual.category_title
        spiritual.delete()
        messages.success(request, f"'{category_title}' has been deleted successfully.")
        return redirect('spiritual')
    
    return render(request, 'admin/spiritual/deletespiritual.html', {
        'spiritual': spiritual
    })


# ============================================
# OFFICE BEARER VIEWS
# ============================================

def officebearer_list(request):
    """Display list of all office bearers with designation filter"""
    designation_filter = request.GET.get('designation', '')
    
    officebearers = Officebearer.objects.select_related('designation').all().order_by('-created_at')
    
    if designation_filter:
        officebearers = officebearers.filter(designation_id=designation_filter)
    
    designations = Designation.objects.all().order_by('name')
    
    return render(request, 'admin/spiritual/officebearer/officebearer.html', {
        'officebearers': officebearers,
        'designations': designations,
        'selected_designation_id': designation_filter,
    })


def add_officebearer(request):
    """Add a new office bearer"""
    if request.method == "POST":
        form = OfficebearerForm(request.POST, request.FILES)
        if form.is_valid():
            officebearer = form.save()
            messages.success(request, f"Office bearer '{officebearer.name}' added successfully!")
            return redirect('officebearer')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OfficebearerForm()
    
    return render(request, 'admin/spiritual/officebearer/addoffice.html', {
        'form': form,
        'designations': Designation.objects.all().order_by('name'),
    })


def edit_officebearer(request, id):
    """Edit an existing office bearer"""
    officebearer = get_object_or_404(Officebearer, id=id)
    
    if request.method == "POST":
        form = OfficebearerForm(request.POST, request.FILES, instance=officebearer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Office bearer '{officebearer.name}' updated successfully!")
            return redirect('officebearer')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = OfficebearerForm(instance=officebearer)
    
    return render(request, 'admin/spiritual/officebearer/editoffice.html', {
        'form': form,
        'officebearer': officebearer,
        'designations': Designation.objects.all().order_by('name'),
    })


def delete_officebearer(request, id):
    """Delete an office bearer"""
    officebearer = get_object_or_404(Officebearer, id=id)
    
    if request.method == "POST":
        name = officebearer.name
        officebearer.delete()
        messages.success(request, f"Office bearer '{name}' has been deleted successfully.")
        return redirect('officebearer')
    
    return render(request, 'admin/spiritual/officebearer/deleteoffice.html', {
        'officebearer': officebearer
    })


def officebearer_detail(request, id):
    """Display details of a specific office bearer"""
    officebearer = get_object_or_404(Officebearer.objects.select_related('designation'), id=id)
    spiritual_categories = officebearer.spiritual_categories.all()
    
    return render(request, 'admin/spiritual/officebearer/officebearer_detail.html', {
        'officebearer': officebearer,
        'spiritual_categories': spiritual_categories,
    })


# ============================================
# COORDINATOR VIEWS (Updated - Many-to-Many)
# ============================================

def coordinator_list(request):
    """Display list of all coordinators with filters"""
    designation_filter = request.GET.get('designation', '')
    spiritual_filter = request.GET.get('spiritual', '')
    
    # Start with all coordinators
    coordinators = Coordinator.objects.select_related('designation').all().order_by('name')
    
    # Apply filters
    if designation_filter:
        coordinators = coordinators.filter(designation_id=designation_filter)
    
    if spiritual_filter:
        coordinators = coordinators.filter(spiritual_categories__id=spiritual_filter)
    
    # Get data for dropdowns
    designations = Designation.objects.all().order_by('name')
    spirituals = Spiritual.objects.all().order_by('category_title')
    
    return render(request, 'admin/spiritual/coordinators/coord.html', {
        'coordinators': coordinators,
        'designations': designations,
        'spirituals': spirituals,
        'selected_designation_id': designation_filter,
        'selected_spiritual_id': spiritual_filter,
    })


def add_coordinator(request):
    """Add a new coordinator"""
    if request.method == "POST":
        form = CoordinatorForm(request.POST, request.FILES)
        if form.is_valid():
            coordinator = form.save()
            messages.success(request, f"Coordinator '{coordinator.name}' added successfully!")
            return redirect('coordinator_list')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Debug
    else:
        form = CoordinatorForm()
    
    return render(request, 'admin/spiritual/coordinators/addcoord.html', {
        'form': form,
        'designations': Designation.objects.all().order_by('name'),
    })


def edit_coordinator(request, id):
    """Edit an existing coordinator"""
    coordinator = get_object_or_404(Coordinator, id=id)
    
    if request.method == "POST":
        form = CoordinatorForm(request.POST, request.FILES, instance=coordinator)
        if form.is_valid():
            form.save()
            messages.success(request, f"Coordinator '{coordinator.name}' updated successfully!")
            return redirect('coordinator_list')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Debug
    else:
        form = CoordinatorForm(instance=coordinator)
    
    return render(request, 'admin/spiritual/coordinators/editcoord.html', {
        'form': form,
        'coordinator': coordinator,
        'designations': Designation.objects.all().order_by('name'),
    })


def delete_coordinator(request, id):
    """Delete a coordinator"""
    coordinator = get_object_or_404(Coordinator, id=id)
    
    if request.method == "POST":
        name = coordinator.name
        coordinator.delete()
        messages.success(request, f"Coordinator '{name}' has been deleted successfully.")
        return redirect('coordinator_list')
    
    return render(request, 'admin/spiritual/coordinators/deletecoord.html', {
        'coordinator': coordinator
    })


def coordinator_detail(request, id):
    """Display details of a specific coordinator"""
    coordinator = get_object_or_404(Coordinator.objects.select_related('designation'), id=id)
    spiritual_categories = coordinator.spiritual_categories.all()
    
    return render(request, 'admin/spiritual/coordinators/coordinator_detail.html', {
        'coordinator': coordinator,
        'spiritual_categories': spiritual_categories,
    })
# ============================================
# API VIEWS (Optional - for AJAX search)
# ============================================

# def search_officebearers(request):
#     """API endpoint to search office bearers by name"""
#     query = request.GET.get('q', '')
#     if query:
#         officebearers = Officebearer.objects.filter(
#             name__icontains=query
#         )[:10]
#         data = [{
#             'id': ob.id,
#             'name': ob.name,
#             'designation': ob.designation,
#             'phone': ob.phone,
#             'email': ob.email,
#             'district': ob.district,
#             'image': ob.image.url if ob.image else None
#         } for ob in officebearers]
#         return JsonResponse(data, safe=False)
#     return JsonResponse([], safe=False)


from django.shortcuts import render, get_object_or_404
from .models import Spiritual

def spiritual_detail(request, slug):
    """
    Display detailed view of a specific spiritual category
    """
    spiritual = get_object_or_404(Spiritual, slug=slug)
    officebearers = spiritual.officebearers.select_related('designation').all().order_by('name')
    coordinators = spiritual.coordinators.select_related('designation').all().order_by('name')
    
    context = {
        'spiritual': spiritual,
        'officebearers': officebearers,
        'coordinators': coordinators,
        'officebearers_count': officebearers.count(),
        'coordinators_count': coordinators.count(),
        'page_title': spiritual.category_title,
        'active_page': 'spiritual'
    }
    return render(request, 'spiritual/detail.html', context)




    # ============================================
# DESIGNATION VIEWS
# ============================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Designation
from .forms import DesignationForm



def designation_list(request):
    designations = Designation.objects.all().order_by('name')

    return render(
        request,
        'admin/spiritual/designation/designation.html',
        {
            'designations': designations
        }
    )



def add_designation(request):

    if request.method == "POST":

        form = DesignationForm(request.POST)

        if form.is_valid():

            designation = form.save()

            messages.success(
                request,
                f"Designation '{designation.name}' added successfully!"
            )

            return redirect('designation')

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = DesignationForm()


    return render(
        request,
        'admin/spiritual/designation/adddesignation.html',
        {
            'form': form
        }
    )



def edit_designation(request, id):
    designation = get_object_or_404(
        Designation,
        id=id
    )
    if request.method == "POST":
        form = DesignationForm(
            request.POST,
            instance=designation
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Designation updated successfully!"
            )
        return redirect('designation')
    else:
        form = DesignationForm(
            instance=designation
        )
    return render(
        request,
        'admin/spiritual/designation/editdesignation.html',
        {
            'form':form,
            'designation':designation
        }
    )
def delete_designation(request,id):

    designation = get_object_or_404(
        Designation,
        id=id
    )
    if request.method=="POST":
        name = designation.name
        designation.delete()
        messages.success(
            request,
            f"Designation '{name}' deleted successfully!"
        )
        return redirect('designation')
    return render(
        request,
        'admin/designation/deletedesignation.html',
        {
            'designation':designation
        }
    )


#KARUNYA SPARSHAM
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify  # <-- ADD THIS IMPORT
from django.contrib.auth.decorators import login_required
from .models import Karunyasparsham, Category
from .forms import KarunyasparshamForm

@login_required
def karunyasparsham_list(request):
    """List all karunyasparsham entries"""
    about_entries = Karunyasparsham.objects.filter(content_type='about')
    project_entries = Karunyasparsham.objects.filter(content_type='project')
    
    context = {
        'about_entries': about_entries,
        'project_entries': project_entries,
        'all_entries': Karunyasparsham.objects.all(),
        'has_about': about_entries.exists(),
        'total_count': Karunyasparsham.objects.count(),
        'about_count': about_entries.count(),
        'project_count': project_entries.count(),
    }
    return render(request, 'admin/karunyam/karunyam.html', context)

@login_required
def karunyasparsham_create(request):
    """Create new karunyasparsham entry"""
    about_exists = Karunyasparsham.objects.filter(content_type='about').exists()
    
    if request.method == 'POST':
        form = KarunyasparshamForm(request.POST, request.FILES)
        
        if form.is_valid():
            content_type = form.cleaned_data.get('content_type')
            
            # Check if trying to create about when it already exists
            if content_type == 'about' and about_exists:
                messages.error(request, 'About section already exists! You can only have one About section. Please edit the existing one.')
                return render(request, 'admin/karunyam/addkarunyam.html', {
                    'form': form,
                    'about_exists': about_exists,
                    'is_edit': False
                })
            
            # Save the instance
            instance = form.save()
            
            messages.success(request, f'{content_type.capitalize()} entry created successfully!')
            return redirect('karunyasparsham_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = KarunyasparshamForm()
    
    return render(request, 'admin/karunyam/addkarunyam.html', {
        'form': form,
        'about_exists': about_exists,
        'is_edit': False
    })

@login_required
def karunyasparsham_edit(request, pk):
    """Edit existing karunyasparsham entry"""
    entry = get_object_or_404(Karunyasparsham, pk=pk)
    about_exists = Karunyasparsham.objects.filter(content_type='about').exclude(pk=pk).exists()
    
    if request.method == 'POST':
        form = KarunyasparshamForm(request.POST, request.FILES, instance=entry)
        
        if form.is_valid():
            content_type = form.cleaned_data.get('content_type')
            
            # Check if trying to change project to about when about already exists
            if content_type == 'about' and about_exists and entry.content_type != 'about':
                messages.error(request, 'About section already exists! You cannot create another one.')
                return render(request, 'admin/karunyam/addkarunyam.html', {
                    'form': form,
                    'entry': entry,
                    'about_exists': about_exists,
                    'is_edit': True
                })
            
            # Save the instance
            instance = form.save()
            
            messages.success(request, f'{content_type.capitalize()} entry updated successfully!')
            return redirect('karunyasparsham_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = KarunyasparshamForm(instance=entry)
    
    return render(request, 'admin/karunyam/addkarunyam.html', {
        'form': form,
        'entry': entry,
        'about_exists': about_exists,
        'is_edit': True
    })

@login_required
def karunyasparsham_delete(request, pk):
    entry = get_object_or_404(Karunyasparsham, pk=pk)

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Entry deleted successfully!")
        return redirect("karunyasparsham_list")

    return redirect("karunyasparsham_list")
def view_karunyam(request, pk):
    """View karunyam entry detail by primary key"""
    entry = get_object_or_404(Karunyasparsham, pk=pk)
    return render(request, 'admin/karunyam/viewkarunyam.html', {'entry': entry})
@login_required
def karunyasparsham_detail(request, slug):
    """View detail by slug"""
    entry = get_object_or_404(Karunyasparsham, slug=slug)
    return render(request, 'admin/karunyam/viewkarunyam.html', {'entry': entry})

@login_required
def karunyasparsham_detail_pk(request, pk):
    """View detail by pk (fallback)"""
    entry = get_object_or_404(Karunyasparsham, pk=pk)
    return render(request, 'admin/karunyam/viewkarunyam.html', {'entry': entry})

@login_required
def get_existing_about(request):
    """Check if about section exists"""
    about_exists = Karunyasparsham.objects.filter(content_type='about').exists()
    about_entries = Karunyasparsham.objects.filter(content_type='about').values('id', 'about_title')
    
    return JsonResponse({
        'about_exists': about_exists,
        'about_entries': list(about_entries)
    })

@login_required
def get_about_options(request):
    """Get about options for dropdown"""
    options = Karunyasparsham.objects.filter(content_type='about')
    options_list = [{'id': opt.id, 'title': opt.about_title} for opt in options]
    
    return JsonResponse({'options': options_list})

@login_required
def get_project_options(request):
    """Get project options for dropdown"""
    options = Karunyasparsham.objects.filter(content_type='project')
    options_list = [{'id': opt.id, 'title': opt.project_title} for opt in options]
    
    return JsonResponse({'options': options_list})

@login_required
def toggle_status(request, pk):
    """Toggle active status of an entry"""
    entry = get_object_or_404(Karunyasparsham, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['inactive', 'completed', 'processing']:
            entry.active = status
            entry.save()
            messages.success(request, f'Status updated to {entry.get_active_display()}')
        
    return redirect('karunyasparsham_list')


#KARUNYAM CATEGORY

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Category
from .forms import CategoryForm

# List View with Search (No Pagination)
def category_list(request):
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(slug__icontains=search_query)
        )
    
    context = {
        'categories': categories,  # Make sure this is 'categories'
        'search_query': search_query,
        'total_count': categories.count(),
    }
    return render(request, 'admin/karunyam/category/category.html', context)

# Create View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Category
from .forms import CategoryForm

# List View with Search (No Pagination)
def category_list(request):
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(slug__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'search_query': search_query,
        'total_count': categories.count(),
    }
    return render(request, 'admin/karunyam/category/category.html', context)

# Create View - Authentication Removed
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/karunyam/category/addcategory.html', {
        'form': form,
        'title': 'Create Category',
        'button_text': 'Create Category'
    })

# Update View - Authentication Removed
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            # Handle image removal
            if request.POST.get('remove_image') == 'true':
                if category.image:
                    category.image.delete(save=False)
                    category.image = None
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/karunyam/category/editcategory.html', {
        'form': form,
        'category': category,
        'title': 'Update Category',
        'button_text': 'Update Category'
    })

# Delete View - Authentication Removed
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        # Delete the image file from storage
        if category.image:
            category.image.delete(save=False)
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'admin/karunyam/category/deletecategory.html', {'category': category})

# Bulk Delete View - Authentication Removed
def category_bulk_delete(request):
    if request.method == 'POST':
        category_ids = request.POST.getlist('category_ids')
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            count = categories.count()
            # Delete images
            for category in categories:
                if category.image:
                    category.image.delete(save=False)
            categories.delete()
            messages.success(request, f'{count} categories deleted successfully!')
        else:
            messages.warning(request, 'No categories selected for deletion.')
    
    return redirect('category_list')

# API-like View to get category data in JSON
def category_api(request):
    categories = Category.objects.all().values('id', 'name', 'slug', 'image')
    return JsonResponse(list(categories), safe=False)


# def category_detail_by_slug(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     return render(request, 'admin/karunyam/category/category.html', {'category': category})


#PUBLICATIONS
from django.shortcuts import render, redirect
from .forms import PublicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Publication
from .forms import PublicationForm

# ========================================
# CREATE PUBLICATION
# ========================================
@login_required
def add_publication(request):
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save()
            messages.success(request, f'Publication "{publication.title}" added successfully!')
            return redirect('publication_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PublicationForm()

    return render(request, "admin/publications/addpublications.html", {
        "form": form
    })

# ========================================
# LIST PUBLICATIONS
# ========================================
@login_required
def publication_list(request):
    publications = Publication.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        publications = publications.filter(title__icontains=search_query)
    
    # Pagination
    paginator = Paginator(publications, 10)  # Show 10 publications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "admin/publications/publications.html", {
        "publications": page_obj,
        "search_query": search_query,
    })

# ========================================
# EDIT PUBLICATION
# ========================================
@login_required
def edit_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, f'Publication "{publication.title}" updated successfully!')
            return redirect('publication_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PublicationForm(instance=publication)
    
    return render(request, "admin/publications/editpublications.html", {
        "form": form,
        "publication": publication
    })

# ========================================
# DELETE PUBLICATION
# ========================================
@login_required
def delete_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    
    if request.method == "POST":
        title = publication.title
        publication.delete()
        messages.success(request, f'Publication "{title}" deleted successfully!')
        return redirect('publication_list')
    
    return render(request, "admin/publications/deletepublications.html", {
        "publication": publication
    })

# ========================================
# VIEW PUBLICATION DETAIL
# ========================================
@login_required
def view_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, "admin/publications/viewpublications.html", {
        "publication": publication
    })



#GALLERY

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Gallery
from .forms import GalleryForm

# ========================================
# PUBLIC VIEWS
# ========================================

def admin_gallery_list(request):
    """Display all active gallery items"""
    gallery_items = Gallery.objects.filter(is_active=True)
    
    # Optional: Filter by media type
    media_type = request.GET.get('type')
    if media_type in ['image', 'video']:
        gallery_items = gallery_items.filter(media_type=media_type)
    
    # Pagination
    paginator = Paginator(gallery_items, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'gallery_items': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'media_type': media_type,
        'total_items': gallery_items.count(),
    }
    return render(request, 'admin/gallery/gallery.html', context)

def gallery_detail(request, slug):
    """Display a single gallery item"""
    gallery_item = get_object_or_404(Gallery, slug=slug, is_active=True)
    
    # Get previous and next items
    previous = Gallery.objects.filter(
        is_active=True, 
        order__lt=gallery_item.order
    ).order_by('-order').first()
    
    next_item = Gallery.objects.filter(
        is_active=True, 
        order__gt=gallery_item.order
    ).order_by('order').first()
    
    context = {
        'item': gallery_item,
        'previous': previous,
        'next': next_item,
    }
    return render(request, 'admin/gallery/gallery_detail.html', context)

# ========================================
# ADMIN VIEWS
# ========================================
# views.py@staff_member_required
def admin_gallery_list(request):
    """Admin view to list all gallery items"""
    gallery_items = Gallery.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        gallery_items = gallery_items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by media type
    media_type = request.GET.get('type')
    if media_type in ['image', 'video']:
        gallery_items = gallery_items.filter(media_type=media_type)
    
    paginator = Paginator(gallery_items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'gallery_items': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
        'media_type': media_type,
        'total_items': gallery_items.count(),
    }
    return render(request, 'admin/gallery/gallery.html', context)

@staff_member_required
def admin_gallery_add(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save()
            messages.success(request, f'Gallery item "{gallery_item.title}" added successfully!')
            return redirect('admin_gallery_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # For debugging
    else:
        form = GalleryForm()
    
    context = {
        'form': form,
        'is_edit': False,
        'title': 'Add Gallery Item',
    }
    return render(request, 'admin/gallery/addgallery.html', context)


@staff_member_required
def admin_gallery_edit(request, pk):
    gallery_item = get_object_or_404(Gallery, pk=pk)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery_item)
        if form.is_valid():
            # Check if the image field was cleared (using ClearableFileInput)
            if 'image' in request.POST and request.POST.get('image-clear', False):
                gallery_item.image.delete(save=False)
                gallery_item.image = None
            
            form.save()
            messages.success(request, f'Gallery item "{gallery_item.title}" updated successfully!')
            return redirect('admin_gallery_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # For debugging
    else:
        form = GalleryForm(instance=gallery_item)
    
    context = {
        'form': form,
        'gallery_item': gallery_item,
        'is_edit': True,
        'title': 'Edit Gallery Item',
    }
    return render(request, 'admin/gallery/editgallery.html', context)


@staff_member_required
def admin_gallery_delete(request, pk):
    gallery_item = get_object_or_404(Gallery, pk=pk)
    
    if request.method == 'POST':
        title = gallery_item.title
        gallery_item.delete()
        messages.success(request, f'Gallery item "{title}" deleted successfully!')
        return redirect('admin_gallery_list')
    
    context = {
        'gallery_item': gallery_item,
    }
    return render(request, 'admin/gallery/deletegallery.html', context)



#PRAYER BOOKS


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import PrayerBook
from .forms import PrayerBookForm
@staff_member_required
def admin_prayerbook_list(request):
    """Admin view to list all prayer books"""
    prayer_books = PrayerBook.objects.all().order_by('title')
    
    search_query = request.GET.get('search', '')
    if search_query:
        prayer_books = prayer_books.filter(title__icontains=search_query)
    
    paginator = Paginator(prayer_books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'prayer_books': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
        'total_items': prayer_books.count(),
    }
    # IMPORTANT: Use the admin template, not the frontend template
    return render(request, 'admin/prayerbooks/prayerbook_list.html', context)

@staff_member_required
def admin_prayerbook_add(request):
    """Add a new prayer book"""
    if request.method == 'POST':
        form = PrayerBookForm(request.POST, request.FILES)
        if form.is_valid():
            prayer_book = form.save()
            messages.success(request, f'Prayer book "{prayer_book.title}" added successfully!')
            return redirect('admin_prayerbook_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PrayerBookForm()
    
    context = {
        'form': form,
        'is_edit': False,
        'title': 'Add Prayer Book',
    }
    return render(request, 'admin/prayerbooks/addprayer.html', context)

@staff_member_required
def admin_prayerbook_edit(request, pk):
    """Edit a prayer book"""
    prayer_book = get_object_or_404(PrayerBook, pk=pk)
    
    if request.method == 'POST':
        form = PrayerBookForm(request.POST, request.FILES, instance=prayer_book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Prayer book "{prayer_book.title}" updated successfully!')
            return redirect('admin_prayerbook_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PrayerBookForm(instance=prayer_book)
    
    context = {
        'form': form,
        'prayer_book': prayer_book,
        'is_edit': True,
        'title': 'Edit Prayer Book',
    }
    return render(request, 'admin/prayerbooks/editprayer.html', context)

@staff_member_required
def admin_prayerbook_delete(request, pk):
    """Delete a prayer book"""
    prayer_book = get_object_or_404(PrayerBook, pk=pk)
    
    if request.method == 'POST':
        title = prayer_book.title
        prayer_book.delete()
        messages.success(request, f'Prayer book "{title}" deleted successfully!')
        return redirect('admin_prayerbook_list')
    
    context = {
        'prayer_book': prayer_book,
    }
    return render(request, 'admin/prayerbooks/deleteprayerbook.html', context)
# KALPANA

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Kalpana, KalpanaFile
from .forms import KalpanaForm, KalpanaFileForm, KalpanaUpdateForm


def kalpana_list(request):
    """List all Kalpana"""

    kalpanas = Kalpana.objects.all().order_by('-created_at')

    return render(
        request,
        'admin/kalpana/kalpana.html',
        {
            'kalpanas': kalpanas,
            'total_count': kalpanas.count()
        }
    )


def kalpana_create(request):
    """
    Create one Kalpana with:

    One Title
        ├── Description 1 → File 1
        ├── Description 2 → File 2
        ├── Description 3 → File 3
        └── etc.
    """

    if request.method == 'POST':

        form = KalpanaForm(request.POST)

        if form.is_valid():

            # Create title
            kalpana = form.save()

            descriptions = request.POST.getlist('descriptions[]')

            file_count = 0

            # IMPORTANT:
            # file_0 belongs to descriptions[0]
            # file_1 belongs to descriptions[1]
            # file_2 belongs to descriptions[2]

            for index, description in enumerate(descriptions):

                description = description.strip()

                if not description:
                    continue

                uploaded_file = request.FILES.get(
                    f'file_{index}'
                )

                if not uploaded_file:
                    continue

                KalpanaFile.objects.create(
                    kalpana=kalpana,
                    file=uploaded_file,
                    description=description,
                    file_name=uploaded_file.name
                )

                file_count += 1

            if file_count > 0:

                messages.success(
                    request,
                    f'Kalpana "{kalpana.title}" created successfully '
                    f'with {file_count} file(s).'
                )

            else:

                messages.warning(
                    request,
                    f'Kalpana "{kalpana.title}" created, '
                    f'but no description/file pairs were added.'
                )

            return redirect('kalpana_list')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = KalpanaForm()

    return render(
        request,
        'admin/kalpana/addkalpana.html',
        {
            'form': form,
            'is_edit': False,
            'action': 'Create',
            'button_text': 'Create Kalpana',
            'kalpana': None
        }
    )


def kalpana_update(request, slug):
    """Update an existing Kalpana"""

    kalpana = get_object_or_404(
        Kalpana,
        slug=slug
    )

    if request.method == 'POST':

        form = KalpanaUpdateForm(
            request.POST,
            instance=kalpana
        )

        if form.is_valid():

            kalpana = form.save()

            # ----------------------------------
            # REMOVE EXISTING FILES
            # ----------------------------------

            removed_files = request.POST.getlist(
                'removed_files[]'
            )

            if removed_files:

                KalpanaFile.objects.filter(
                    id__in=removed_files,
                    kalpana=kalpana
                ).delete()

            # ----------------------------------
            # UPDATE EXISTING FILE DESCRIPTIONS
            # ----------------------------------

            existing_files = kalpana.files.all()

            for file_obj in existing_files:

                if str(file_obj.id) in removed_files:
                    continue

                new_description = request.POST.get(
                    f'file_description_{file_obj.id}',
                    ''
                ).strip()

                new_file_name = request.POST.get(
                    f'file_name_{file_obj.id}',
                    ''
                ).strip()

                file_obj.description = new_description

                if new_file_name:
                    file_obj.file_name = new_file_name

                file_obj.save()

            # ----------------------------------
            # ADD NEW DESCRIPTION + FILE PAIRS
            # ----------------------------------

            descriptions = request.POST.getlist(
                'descriptions[]'
            )

            new_file_count = 0

            for index, description in enumerate(descriptions):

                description = description.strip()

                if not description:
                    continue

                uploaded_file = request.FILES.get(
                    f'file_{index}'
                )

                if not uploaded_file:
                    continue

                KalpanaFile.objects.create(
                    kalpana=kalpana,
                    file=uploaded_file,
                    description=description,
                    file_name=uploaded_file.name
                )

                new_file_count += 1

            messages.success(
                request,
                f'Kalpana "{kalpana.title}" updated successfully!'
            )

            return redirect('kalpana_list')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = KalpanaUpdateForm(
            instance=kalpana
        )

    existing_files = kalpana.files.all()

    return render(
        request,
        'admin/kalpana/editkalpana.html',
        {
            'form': form,
            'is_edit': True,
            'action': 'Update',
            'button_text': 'Update Kalpana',
            'kalpana': kalpana,
            'existing_files': existing_files
        }
    )


def kalpana_delete(request, slug):
    """Delete an entire Kalpana"""

    kalpana = get_object_or_404(
        Kalpana,
        slug=slug
    )

    if request.method == 'POST':

        title = kalpana.title

        kalpana.files.all().delete()
        kalpana.delete()

        messages.success(
            request,
            f'Kalpana "{title}" deleted successfully!'
        )

        return redirect('kalpana_list')

    return render(
        request,
        'admin/kalpana/deletekalpana.html',
        {
            'kalpana': kalpana
        }
    )


def kalpana_delete_file(request, file_id):
    """Delete one Kalpana file"""

    file_obj = get_object_or_404(
        KalpanaFile,
        id=file_id
    )

    kalpana_slug = file_obj.kalpana.slug

    if request.method == 'POST':

        file_obj.delete()

        messages.success(
            request,
            'File removed successfully!'
        )

    return redirect(
        'kalpana_update',
        slug=kalpana_slug
    )



# EVENTSfrom django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Event
from .forms import EventForm

# Admin: List all events
@staff_member_required
def event_list(request):
    events = Event.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(location__icontains=search_query)
        )
    
    filter_status = request.GET.get('filter', '')
    now = timezone.now()
    if filter_status == 'upcoming':
        events = events.filter(
            Q(event_date__gt=now.date()) | 
            (Q(event_date=now.date()) & Q(event_time__gt=now.time()))
        )
    elif filter_status == 'past':
        events = events.filter(
            Q(event_date__lt=now.date()) | 
            (Q(event_date=now.date()) & Q(event_time__lt=now.time()))
        )
    elif filter_status == 'today':
        events = events.filter(event_date=now.date())
    
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'search_query': search_query,
        'filter_status': filter_status,
        'total_items': Event.objects.count(),
        'upcoming_count': Event.objects.filter(
            Q(event_date__gt=now.date()) | 
            (Q(event_date=now.date()) & Q(event_time__gt=now.time()))
        ).count(),
        'past_count': Event.objects.filter(
            Q(event_date__lt=now.date()) | 
            (Q(event_date=now.date()) & Q(event_time__lt=now.time()))
        ).count(),
    }
    return render(request, 'admin/events/events.html', context)

# Admin: Add event
@staff_member_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('event_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()
    
    context = {
        'form': form,
        'event': None,
    }
    return render(request, 'admin/events/addevents.html', context)

# Admin: Edit event
@staff_member_required
def event_edit(request):
    event_id = request.GET.get('id')
    if not event_id:
        messages.error(request, 'No event specified for editing.')
        return redirect('event_list')
    
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" updated successfully!')
            return redirect('event_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'admin/events/editevents.html', context)

# Admin: Delete event
@staff_member_required
def event_delete(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        if not event_id:
            messages.error(request, 'No event specified for deletion.')
            return redirect('event_list')
        
        event = get_object_or_404(Event, pk=event_id)
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" deleted successfully!')
        return redirect('event_list')
    
    # If GET request, redirect to list
    return redirect('event_list')


#DOWNLOADS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Download
from .forms import DownloadForm

# ==================== PUBLIC VIEWS ====================
# views.py (updated)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from .models import Download
from .forms import DownloadForm

def downloads(request):
    """Public downloads page"""

    # Get all downloads from database
    all_downloads = Download.objects.all()

    # Get specific document types
    church_account_manual = Download.objects.filter(
        document_type='church_account_manual'
    ).first()

    constitution_1934 = Download.objects.filter(
        document_type='constitution_1934'
    ).first()

    guidelines = Download.objects.filter(
        document_type='guidelines'
    ).first()

    context = {
        'downloads': all_downloads,
        'church_account_manual': church_account_manual,
        'constitution_1934': constitution_1934,
        'guidelines': guidelines,
        'page_title': 'Downloads',
        'additional_info': 'Download our resources and documents',
    }

    return render(request, 'media/downloads.html', context)


# ==================== ADMIN VIEWS ====================

@staff_member_required
def admin_download_list(request):
    """Admin: List all downloads"""

    downloads = Download.objects.all().order_by('document_type')

    search_query = request.GET.get('search', '')

    if search_query:
        downloads = downloads.filter(
            Q(document_type__icontains=search_query) |
            Q(file__icontains=search_query)
        )

    paginator = Paginator(downloads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'downloads': page_obj,
        'search_query': search_query,
        'total_items': Download.objects.count(),
    }

    return render(
        request,
        'admin/downloads/downloads.html',
        context
    )


@staff_member_required
def admin_download_add(request):
    """Admin: Add new download"""

    if request.method == 'POST':
        form = DownloadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Download added successfully!'
            )
            return redirect('admin_download_list')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = DownloadForm()

    context = {
        'form': form,
        'is_edit': False,
        'title': 'Add New Download',
        'download': None,
    }

    return render(
        request,
        'admin/downloads/adddownloads.html',
        context
    )


@staff_member_required
def admin_download_edit(request, pk):
    """Admin: Edit download"""

    download = get_object_or_404(Download, pk=pk)

    if request.method == 'POST':
        form = DownloadForm(
            request.POST,
            request.FILES,
            instance=download
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Download updated successfully!'
            )
            return redirect('admin_download_list')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = DownloadForm(instance=download)

    context = {
        'form': form,
        'is_edit': True,
        'title': 'Edit Download',
        'download': download,
    }

    return render(
        request,
        'admin/downloads/editdownloads.html',
        context
    )


@staff_member_required
def admin_download_delete(request, pk):
    """Admin: Delete download"""

    download = get_object_or_404(Download, pk=pk)

    if request.method == 'POST':

        # Delete the file from storage
        if download.file:
            download.file.delete(save=False)

        download.delete()

        messages.success(
            request,
            'Download deleted successfully!'
        )

        return redirect('admin_download_list')

    context = {
        'download': download
    }

    return render(
        request,
        'admin/downloads/delete_confirm.html',
        context
    )

from django.http import FileResponse
from django.shortcuts import get_object_or_404

def guideline(request):
    guideline_file = get_object_or_404(
        Download,
        document_type='guidelines'
    )

    return FileResponse(
        guideline_file.file.open('rb'),
        as_attachment=False
    )




#SYNOD

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Synod
from .forms import SynodForm


# =========================================================
# ADD SYNOD
# =========================================================

def add_synod(request):

    if request.method == 'POST':
        form = SynodForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Synod added successfully.'
            )

            return redirect('view_synod')

    else:
        form = SynodForm()

    return render(
        request,
        'admin/synod/addsynod.html',
        {
            'form': form
        }
    )


# =========================================================
# EDIT SYNOD
# =========================================================

def edit_synod(request, slug):

    synod = get_object_or_404(
        Synod,
        slug=slug
    )

    if request.method == 'POST':

        form = SynodForm(
            request.POST,
            request.FILES,
            instance=synod
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Synod updated successfully.'
            )

            return redirect('view_synod')

    else:

        form = SynodForm(
            instance=synod
        )

    return render(
        request,
        'admin/synod/editsynod.html',
        {
            'form': form,
            'synod': synod
        }
    )


# =========================================================
# VIEW SYNODS
# =========================================================

def view_synod(request):

    synods = Synod.objects.all().order_by('name')

    return render(
        request,
        'admin/synod/viewsynod.html',
        {
            'synods': synods
        }
    )


# =========================================================
# DELETE SYNOD
# =========================================================

def delete_synod(request, slug):

    synod = get_object_or_404(
        Synod,
        slug=slug
    )

    if request.method == 'POST':

        # Delete image from storage
        if synod.image:
            synod.image.delete(save=False)

        synod.delete()

        messages.success(
            request,
            'Synod deleted successfully.'
        )

        return redirect('view_synod')

    return render(
        request,
        'admin/synod/deletesynod.html',
        {
            'synod': synod
        }
    )
