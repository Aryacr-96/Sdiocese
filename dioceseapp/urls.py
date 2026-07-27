
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
    path('synod',views.synod,name='synod'),
    path('synod_detail',views.synod_detail,name='synod_detail'),
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
    path('parish-details/<slug:slug>/',views.parish_details,name='parish_details'
),


        
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
    path('projects/',views.projects,name='projects'),
    path('projects_detail/',views.projects_detail,name='projects_detail'),
    


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
    path('calendar/',views.calendar,name='calendar'),
     path('events/',views.events,name='events'),

    #DOWNLOADS

    path('kalpana/',views.kalpana,name='kalpana'),
    path('kalpanadetail/',views.kalpanadetail,name='kalpanadetail'), 
    path('guideline/',views.guideline,name='guideline'),
    path('prayerbook/',views.prayerbook,name='prayerbook'),
    path('prayerbook/',views.prayerbook,name='prayerbook'),
    


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
    path('admin/spiritual/delete/<int:id>/', views.delete_spiritual, name='delete_spiritual'),
    path('admin/spiritual/detail/<int:id>/', views.spiritual_detail, name='spiritual_detail'),
    
    # OFFICE BEARER ADMIN
    path('admin/officebearer/', views.officebearer_list, name='officebearer'),
    path('admin/officebearer/add/', views.add_officebearer, name='add_officebearer'),
    path('admin/officebearer/edit/<int:id>/', views.edit_officebearer, name='edit_officebearer'),
    path('admin/officebearer/delete/<int:id>/', views.delete_officebearer, name='delete_officebearer'),
    path('admin/officebearer/detail/<int:id>/', views.officebearer_detail, name='officebearer_detail'),

    # API ENDPOINT FOR SEARCH (Optional)
    # path('api/officebearers/search/', views.search_officebearers, name='search_officebearers'),

]