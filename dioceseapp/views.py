from django.urls import path
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

# ADD THESE IMPORTS:
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from .forms import adminform 


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
def synod(request):
    return render(request,'about/synod.html')
def throne(request):
    return render(request,'about/throne.html')
def synod_detail(request):
    return render(request,'about/synod_detail.html')

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
    return render(request,'karunyam/karunyam.html')
def projects(request):
    return render(request,'karunyam/projects.html')
def projects_detail(request):
    return render(request,'karunyam/projectsdetail.html')



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


def publications(request):
    return render(request,'media/publications.html')
def images(request):
    return render(request,'media/images.html')
def videos(request):
    return render(request,'media/videos.html')
def calendar(request):
    return render(request,'media/calendar.html')
def events(request):
    return render(request,'media/events.html')


# DOWNLOADS

def kalpana(request):
    return render(request,'downloads/kalpana.html')
def kalpanadetail(request):
    return render(request,'downloads/kalpanadetail.html')
def guideline(request):
    return render(request,'downloads/guidelines.html')
def prayerbook(request):
    return render(request,'downloads/prayerbooks.html')




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
from .models import Priest,Parish
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
            form.save()
            return redirect('admin_priests')
    else:
        form = PriestForm()

    return render(request, 'admin/priest/addpriest.html', {
        'form': form,
    })


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
            return redirect('admin_priests')
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
        priest.delete()
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

            parish.save()

            return redirect('admin_parishes')

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

    return render(request, 'admin/parish/viewparish.html', {
        'parish': parish,
        'embed_url': embed_url,
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



from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm


# Contact List
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


# Contact Delete
def contactdelete(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        contact.delete()
        return redirect('contact')

    context = {
        'contact': contact
    }
    return render(request, 'admin/contact/contactdelete.html', context)
