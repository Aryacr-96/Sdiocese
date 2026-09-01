
from tokenize import Single
from django.urls import path

from dioceseapp import views

urlpatterns = [
    
   # Admin Login
    path('admin/', views.admin, name='admin'),

    # Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Logout
    path('admin/logout/', views.logoutadmin, name='logoutadmin'),

    # ABOUT CHURCH

    path('admin/', views.admin, name='admin'),
    path('',views.index,name='index'),
    path('believe',views.believe,name='believe'),
    path('catholicate',views.catholicate,name='catholicate'),
    path('history',views.history,name='history'),
    path('malankara',views.malankara,name='malankara'),
    path(
    'synod/',
    views.synod,
    name='synod'
),

path(
    'synod/<slug:slug>/',
    views.synod_detail,
    name='synod_detail'
),
    path('throne',views.throne,name='throne'),
    
    # ABOUT DIOCESE
   
    
    path('batherydiocese/',views.batherydiocese,name='batherydiocese'),
    path('committe/',views.committe,name='committe'),
    path('council/',views.council,name='council'),
    path('diocesehistory/',views.diocesehistory,name='diocesehistory'),
    path('metropolitans/',views.metropolitans,name='metropolitans'),
    path('priest/',views.priest,name='priest'),
    path('priest_details/<slug:slug>/', views.priest_details, name='priest_details'),
    path('priestretired_details/<slug:slug>/',views.priestretired_details,name='priestretired_details'),
    path('parish/', views.parish, name='parish'),
    path('parish/<slug:slug>/', views.parish_details, name='parish_details'),
    path('parish/id/<int:parish_id>/', views.parish_details_by_id, name='parish_details_by_id'),


        
    # SPIRITUAL ORGANIZATIONS

    
    path('vaidika/',views.vaidika,name='vaidika'),
    path('sundayschool/',views.sundayschool,name='sundayschool'),
    path('vanitha/',views.vanitha,name='vanitha'),
    path('prarthana/',views.prarthana,name='prarthana'),
    path('mgocsm/',views.mgocsm,name='mgocsm'),
    path('baskiyoma/',views.baskiyoma,name='baskiyoma'),
    path('ocym/',views.ocym,name='ocym'),
    path('sushrushaka/',views.sushrushaka,name='sushrushaka'),
    path('balika/',views.balika,name='balika'),
    path('human/',views.human,name='human'),
    path('divya/',views.divya,name='divya'),
    path('suvishesham/',views.suvishesham,name='suvishesham'),
    path('sdof/',views.sdof,name='sdof'),
    path('sjof/',views.sjof,name='sjof'),
    


    #KARUNYA SPARSAM

    path('karunyam/',views.karunyam,name='karunyam'),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.projects_detail, name="projects_detail"),
    


    #INSTITUTIONS

    path('school/',views.school,name='school'),
    path('school_detail/',views.school_detail,name='school_detail'),
    path('college/',views.college,name='college'),
    path('college_detail/',views.college_detail,name='college_detail'),
    path('retreat/',views.retreat,name='retreat'),
    path('retreat_detail/',views.retreat_detail,name='retreat_detail'),

    

    #MEDIA


    path('publications/',views.publications,name='publications'),
    path('images/',views.images,name='images'),
    path('videos/',views.videos,name='videos'),
    path('events/', views.events, name='events'),  
    path('calendar/', views.calendar, name='calendar'),

    #DOWNLOADS

    path('kalpana/', views.kalpana, name='kalpana'),
    path('kalpanadetail/<slug:slug>/', views.kalpanadetail, name='kalpanadetail'),
    path('kalpana/file/<int:file_id>/', views.kalpana_view_file, name='kalpana_view_file'),
    path('guideline/',views.guideline,name='guideline'),
    path('prayerbook/', views.prayerbook, name='prayerbook'),
    path('prayerbook-view-file/<int:file_id>/', views.prayerbook_view_file, name='prayerbook_view_file'),
    

#SYNOD DETAIL PAGE

   
   



    # CONTACT

    path('contact/',views.contact,name='contact'),

    # PRIEST ADMIN(
    path('admin/priest/',views.priests,name='admin_priests'),
    path('admin/priest/add/',views.add_priest,name='add_priest'),
    path('admin/priest/view/<int:priest_id>/',views.view_priest,name='view_priest'),
    path('admin/priest/edit/<int:priest_id>/',views.edit_priest,name='edit_priest'),
    path('admin/priest/delete/<int:priest_id>/',views.delete_priest,name='delete_priest'),

    
    # PARISH ADMIN
    path('admin/parish/',views.parishes,name='admin_parishes'),
    path('admin/parish/add/',views.add_parish,name='add_parish'),
    path('admin/parish/view/<int:parish_id>/',views.view_parish,name='view_parish'),
    path('admin/parish/edit/<int:parish_id>/',views.edit_parish,name='edit_parish'),
    path('admin/parish/delete/<int:parish_id>/',views.delete_parish,name='delete_parish'), 

    #CONTACT ADMIN
    path('admin/contact/', views.contactpage, name='contactpage'),
    path('admin/contact/<int:id>/', views.contactview, name='contactview'),
    path('admin/contact/delete/<int:id>/', views.contactdelete, name='contactdelete'),


    # SPIRITUAL ADMIN

    # SPIRITUAL ADMIN
    path('admin/spiritual/', views.spiritual_list, name='spiritual'),
    path('admin/spiritual/add/', views.add_spiritual, name='add_spiritual'),
    path('admin/spiritual/edit/<int:id>/', views.edit_spiritual, name='edit_spiritual'),
     path('admin/spiritual/view/<int:id>/', views.view_spiritual, name='view_spiritual'),
    path('admin/spiritual/delete/<int:id>/', views.delete_spiritual, name='delete_spiritual'),
    path('admin/spiritual/detail/<int:id>/', views.spiritual_detail, name='spiritual_detail'),


    path('spiritual/<slug:slug>/', views.spiritual_detail, name='spiritual_detail'),  # Changed from id to slug

    
    # OFFICE BEARER ADMIN
    path('admin/officebearer/', views.officebearer_list, name='officebearer'),
    path('admin/officebearer/add/', views.add_officebearer, name='add_officebearer'),
    path('admin/officebearer/edit/<int:id>/', views.edit_officebearer, name='edit_officebearer'),
    path('admin/officebearer/delete/<int:id>/', views.delete_officebearer, name='delete_officebearer'),
    path('admin/officebearer/detail/<int:id>/', views.officebearer_detail, name='officebearer_detail'),



    #DESIGNATION
    path('designation/',views.designation_list,name='designation'),
    path('designation/add/',views.add_designation,name='add_designation'),

    path(
        'designation/edit/<int:id>/',
        views.edit_designation,
        name='edit_designation'
    ),

    path(
        'designation/delete/<int:id>/',
        views.delete_designation,
        name='delete_designation'
    ),

    #COORDINATORS
    path('coordinators/', views.coordinator_list, name='coordinator_list'),
    path('coordinators/add/', views.add_coordinator, name='add_coordinator'),
    path('coordinators/edit/<int:id>/', views.edit_coordinator, name='edit_coordinator'),
    path('coordinators/delete/<int:id>/', views.delete_coordinator, name='delete_coordinator'),
    # path('coordinators/detail/<int:id>/', views.coordinator_detail, name='coordinator_detail'),
    # API ENDPOINT FOR SEARCH (Optional)
    # path('api/officebearers/search/', views.search_officebearers, name='search_officebearers'),


    #KARUNYA SPARSHAM
    path('karunyasparsham_list/', views.karunyasparsham_list, name='karunyasparsham_list'),
    path('karunyasparsham_create/', views.karunyasparsham_create, name='karunyasparsham_create'),
    
    # Edit and delete
    path('karunyasparsham_edit/<int:pk>/', views.karunyasparsham_edit, name='karunyasparsham_edit'),
    path('karunyasparsham_delete/<int:pk>/', views.karunyasparsham_delete, name='karunyasparsham_delete'),
    
    # Detail views
    path('karunyasparsham_detail/<slug:slug>/', views.karunyasparsham_detail, name='karunyasparsham_detail'),
    path('karunyasparsham_detail_pk/<int:pk>/', views.karunyasparsham_detail_pk, name='karunyasparsham_detail_pk'),
    
    # API endpoints
    path('api/about-exists/', views.get_existing_about, name='about_exists'),
    path('api/about-options/', views.get_about_options, name='about_options'),
    path('api/project-options/', views.get_project_options, name='project_options'),
    
    # Status toggle
    path('toggle-status/<int:pk>/', views.toggle_status, name='toggle_status'),

    #KARUNYAM CATEGORY
    path('category_list/', views.category_list, name='category_list'),
    
    # Create
    path('create/', views.category_create, name='category_create'),
    
  
    
    # Update
    path('<int:pk>/update/', views.category_update, name='category_update'),
    
    # Delete
    path('<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Bulk actions
    path('bulk-delete/', views.category_bulk_delete, name='category_bulk_delete'),


    #PUBLICATION ADMIN
    # List all publications
    path('admin/publications/', views.publication_list, name='publication_list'),
    
    # Add new publication
    path('admin/publication/add/', views.add_publication, name='add_publication'),
    
    # View publication details
    path('admin/publication/<int:pk>/', views.view_publication, name='view_publication'),
    
    # Edit publication
    path('admin/publication/<int:pk>/edit/', views.edit_publication, name='edit_publication'),
    
    # Delete publication
    path('admin/publication/<int:pk>/delete/', views.delete_publication, name='delete_publication'),

  #GALLERY
     # Admin URLs
    path('admin/gallery/', views.admin_gallery_list, name='admin_gallery_list'),
    path('admin/gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('admin/gallery/edit/<int:pk>/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('admin/gallery/delete/<int:pk>/', views.admin_gallery_delete, name='admin_gallery_delete'),



    #PRAYER BOOKS
      # Admin Prayer Books - MUST come before any wildcard patterns
    path('admin/prayerbooks/', views.admin_prayerbook_list, name='admin_prayerbook_list'),
    path('admin/prayerbooks/add/', views.admin_prayerbook_add, name='admin_prayerbook_add'),
    path('admin/prayerbooks/edit/<int:pk>/', views.admin_prayerbook_edit, name='admin_prayerbook_edit'),
    path('admin/prayerbooks/delete/<int:pk>/', views.admin_prayerbook_delete, name='admin_prayerbook_delete'),


    #KALPANA
   

    path('admin/kalpana_list/', views.kalpana_list, name='kalpana_list'),
    path('admin/kalpana_create/', views.kalpana_create, name='kalpana_create'),
    path('admin/update/<slug:slug>/', views.kalpana_update, name='kalpana_update'),
    path('admin/kalpana_delete/<slug:slug>/', views.kalpana_delete, name='kalpana_delete'),
    
    

    #EVENTS
    
    path('admin/event_list/', views.event_list, name='event_list'),
    path('admin/event_add/', views.event_add, name='event_add'),
    path('admin/event_edit/', views.event_edit, name='event_edit'),
    path('admin/event_delete/', views.event_delete, name='event_delete'),


    #DOWNLOADS

    
    path('admin/downloads/list/', views.admin_download_list, name='admin_download_list'),
    path('admin/downloads/add/', views.admin_download_add, name='admin_download_add'),
    path('admin/downloads/edit/<int:pk>/', views.admin_download_edit, name='admin_download_edit'),
    path('admin/downloads/delete/<int:pk>/', views.admin_download_delete, name='admin_download_delete'),



      # SYNOD
    # =====================================================

    path(
        'add-synod/',
        views.add_synod,
        name='add_synod'
    ),

    path(
        'view-synod/',
        views.view_synod,
        name='view_synod'
    ),

    path(
        'edit-synod/<slug:slug>/',
        views.edit_synod,
        name='edit_synod'
    ),

    path(
        'delete-synod/<slug:slug>/',
        views.delete_synod,
        name='delete_synod'
    ), 
]
    
