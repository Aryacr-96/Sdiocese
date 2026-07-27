from django.urls import path
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

# ADD THESE IMPORTS:
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from .forms import OfficebearerForm, SpiritualForm, adminform 
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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Spiritual, Officebearer, SpiritualOfficeBearer
from .forms import (
    SpiritualForm, 
    OfficebearerForm, 
    NewOfficeBearerForm,
    SpiritualOfficeBearerFormSet
)

# ============================================
# SPIRITUAL VIEWS
# ============================================

def spiritual_list(request):
    """Display list of all spiritual categories"""
    spirituals = Spiritual.objects.all().order_by('-created_at')
    total_bearers = SpiritualOfficeBearer.objects.count()
    
    return render(request, 'admin/spiritual/spiritual.html', {
        'spirituals': spirituals,
        'total_bearers': total_bearers
    })

def spiritual_detail(request, id):
    """Display details of a specific spiritual category"""
    spiritual = get_object_or_404(Spiritual, id=id)
    officebearers = spiritual.officebearers.all()
    
    return render(request, 'admin/spiritual/spiritual_detail.html', {
        'spiritual': spiritual,
        'officebearers': officebearers
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Spiritual, Officebearer, SpiritualOfficeBearer
from .forms import SpiritualForm

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
            
            # Handle new office bearers with images
            new_names = request.POST.getlist('new_officebearer_name[]')
            new_designations = request.POST.getlist('new_officebearer_designation[]')
            new_phones = request.POST.getlist('new_officebearer_phone[]')
            new_emails = request.POST.getlist('new_officebearer_email[]')
            new_districts = request.POST.getlist('new_officebearer_district[]')
            
            # IMPORTANT: Get the image files - they come as a list of files
            new_images = request.FILES.getlist('new_officebearer_image[]')
            
            for i in range(len(new_names)):
                name = new_names[i].strip()
                if name:  # Only create if name is provided
                    # Create office bearer
                    officebearer = Officebearer(
                        name=name,
                        designation=new_designations[i].strip() if i < len(new_designations) else '',
                        phone=new_phones[i].strip() if i < len(new_phones) else '',
                        email=new_emails[i].strip() if i < len(new_emails) else '',
                        district=new_districts[i].strip() if i < len(new_districts) else '',
                    )
                    
                    # Handle image for this office bearer
                    # The images are in the same order as the names
                    if i < len(new_images) and new_images[i]:
                        officebearer.image = new_images[i]
                    
                    # Save the office bearer with image
                    officebearer.save()
                    
                    # Create the association
                    SpiritualOfficeBearer.objects.create(
                        spiritual=spiritual,
                        officebearer=officebearer
                    )
            
            messages.success(request, "Spiritual category added successfully!")
            return redirect('spiritual')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SpiritualForm()
    
    existing_bearers = Officebearer.objects.all().order_by('name')
    selected_bearers = []
    
    return render(request, 'admin/spiritual/addspiritual.html', {
        'form': form,
        'existing_bearers': existing_bearers,
        'selected_bearers': selected_bearers,
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
                    officebearer = Officebearer(
                        name=name,
                        designation=new_designations[i].strip() if i < len(new_designations) else '',
                        phone=new_phones[i].strip() if i < len(new_phones) else '',
                        email=new_emails[i].strip() if i < len(new_emails) else '',
                        district=new_districts[i].strip() if i < len(new_districts) else '',
                    )
                    
                    # Handle image for this office bearer
                    if i < len(new_images) and new_images[i]:
                        officebearer.image = new_images[i]
                    
                    officebearer.save()
                    
                    SpiritualOfficeBearer.objects.create(
                        spiritual=spiritual,
                        officebearer=officebearer
                    )
            
            messages.success(request, "Spiritual category updated successfully!")
            return redirect('spiritual')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SpiritualForm(instance=spiritual)
    
    existing_bearers = Officebearer.objects.all().order_by('name')
    selected_bearers = spiritual.officebearers.values_list('id', flat=True)
    
    return render(request, 'admin/spiritual/addspiritual.html', {
        'form': form,
        'existing_bearers': existing_bearers,
        'selected_bearers': selected_bearers,
        'editing': True,
        'spiritual': spiritual
    })

def delete_spiritual(request, id):
    """Delete a spiritual category"""
    spiritual = get_object_or_404(Spiritual, id=id)
    
    if request.method == "POST":
        category_title = spiritual.category_title
        spiritual.delete()
        messages.success(request, f"'{category_title}' has been deleted successfully.")
        return redirect('spiritual')
    
    return render(request, 'admin/spiritual/delete_spiritual.html', {
        'spiritual': spiritual
    })


# ============================================
# OFFICE BEARER VIEWS
# ============================================

def officebearer_list(request):
    """Display list of all office bearers"""
    officebearers = Officebearer.objects.all().order_by('-created_at')
    return render(request, 'admin/spiritual/officebearer/officebearer.html', {
        'officebearers': officebearers
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
        'form': form
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
        'officebearer': officebearer
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
    officebearer = get_object_or_404(Officebearer, id=id)
    spiritual_categories = officebearer.spiritual_categories.all()
    
    return render(request, 'admin/spiritual/officebearer/officebearer_detail.html', {
        'officebearer': officebearer,
        'spiritual_categories': spiritual_categories
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