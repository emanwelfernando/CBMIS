from django.urls import path
from django.contrib import admin
from barangayApp import provincialAdminviews, municipalAdminviews, barangayAdminviews, barangayStaffviews, views, touristSpotsviews, superAdminviews
from django.views.generic.base import RedirectView
from .provincialAdminviews import ExportResidentsPDFView
from .barangayStaffviews import ExportHouseholdsPDFView, GeneratePDF, ExportHouseholdsExcelView, GenerateExcel
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"), 

    path('', views.home_page, name='home-page'),
    path('map-page', views.map_page, name='map-page'),
    path('<int:id>/', views.tourist_spot_detail, name='tourist_spot_detail'),
    path('add/', views.add_tourist_spot, name='add_tourist_spot'),
    path('<int:id>/edit/', views.edit_tourist_spot, name='edit_tourist_spot'),
    path('logout/', views.logoutUser, name='logout'),
    path('export-residents/', ExportResidentsPDFView.as_view(), name='export-residents'),
    
    # Super Admin URLs
    path('super-admin/dashboard/', login_required(superAdminviews.dashboard), name='super-admin-dashboard'),
    path('super-admin/household/', superAdminviews.household, name='super-admin-household'),
    path('super-admin/household/page/<int:page>/', superAdminviews.household, name='super-admin-household-page'),
    path('super-admin/resident/', superAdminviews.resident, name='super-admin-resident'),
    path('super-admin/resident/page/<int:page>/', superAdminviews.resident, name='super-admin-resident-page'),
    path('super-admin/manage-user/', superAdminviews.manage_users, name='super-admin-manage-user'),
    path('super-admin/manage-user/page/<int:page>/', superAdminviews.manage_users, name='super-admin-manage-user-page'),
    path('super-admin/edit_user/<int:pk>/', superAdminviews.edit_user, name='super-admin-edit-user'),
    path('super-admin/document/', superAdminviews.user_settings, name='super-admin-document'),
    path('super-admin/logout/', superAdminviews.logout),
    path('super-admin/audit-trail/', superAdminviews.audit_log_view, name='super-admin-audit-trail'),
    path('super-admin/register/', superAdminviews.register, name='super-admin-user-register'),
    path('super-admin/edit-user/<int:user_id>/password/', superAdminviews.change_password, name='edit-user-password'),
     
    # Provincial Admin URLs
    path('provincial-admin/dashboard/', provincialAdminviews.dashboard, name='provincial-admin-dashboard'),
    path('provincial-admin/household/', provincialAdminviews.household, name='provincial-admin-household'),
    path('provincial-admin/household/page/<int:page>/', provincialAdminviews.household, name='provincial-admin-household-page'),
    path('provincial-admin/resident/', provincialAdminviews.resident, name='provincial-admin-resident'),
    path('provincial-admin/resident/page/<int:page>/', provincialAdminviews.resident, name='provincial-admin-resident-page'),
    path('provincial-admin/manage-user/', provincialAdminviews.manage_users, name='provincial-admin-manage-user'),
    path('provincial-admin/manage-user/page/<int:page>/', provincialAdminviews.manage_users, name='provincial-admin-manage-user-page'),
    path('provincial-admin/edit_user/<int:pk>/', provincialAdminviews.edit_user, name='provincial-admin-edit-user'),
    path('provincial-admin/document/', provincialAdminviews.user_settings, name='provincial-admin-document'),
    path('provincial-admin/logout/', provincialAdminviews.logout),
    path('provincial-admin/audit-trail/', provincialAdminviews.audit_log_view, name='provincial-admin-audit-trail'),
    path('provincial-admin/register/', provincialAdminviews.register, name='provincial-admin-user-register'),
    path('provincial-admin/edit-user/<int:user_id>/password/', provincialAdminviews.change_password, name='edit-user-password'),
   
    # Municipal Admin URLs
    path('municipal-admin/dashboard/', municipalAdminviews.dashboard, name='municipal-admin-dashboard'),
    path('municipal-admin/barangay/', municipalAdminviews.barangay, name='municipal-admin-barangay'),
    path('municipal-admin/household/', municipalAdminviews.household, name='municipal-admin-household'),
    path('municipal-admin/resident/', municipalAdminviews.resident, name='municipal-admin-resident'),
    path('municipal-admin/register/', municipalAdminviews.register, name='municipal-admin-user-register'),
    path('municipal-admin/manage-user/', municipalAdminviews.manage_users, name='municipal-admin-manage-user'),
    path('municipal-admin/manage-user/page/<int:page>/', municipalAdminviews.manage_users, name='municipal-admin-manage-user-page'),
    path('municipal-admin/edit-user/<int:user_id>/password/', municipalAdminviews.edit_user, name='municipal-admin-edit-user'),
    path('municipal-admin/logout/', municipalAdminviews.logout),

   # Barangay Admin URLs
    path('barangay-admin/dashboard/', barangayAdminviews.dashboard, name='barangay-admin-dashboard'),
    path('barangay-admin/household/', barangayAdminviews.household, name='barangay-admin-household'),
    path('barangay-admin/resident/', barangayAdminviews.resident, name='barangay-admin-resident'),
    path('barangay-admin/user-settings/', barangayAdminviews.user_settings, name='barangay-admin-user-settings'),
    path('barangay-admin/settings/', barangayAdminviews.settings),
    path('barangay-admin/logout/', barangayAdminviews.logout),
    path('barangay-admin/add_resident/', barangayStaffviews.add_resident, name='barangay-admin-add_resident'),
    path('barangay-admin/edit_resident/<str:pk>/', barangayStaffviews.edit_resident, name='barangay-admin-edit-resident'),
    path('barangay-admin/delete_resident/<str:pk>/', barangayStaffviews.delete_resident, name='barangay-admiin-delete-resident'),

    # Barangay Staff URLs
    path('barangay-staff/dashboard/', barangayStaffviews.dashboard, name='barangay-staff-dashboard'),
    path('barangay-staff/household/', barangayStaffviews.household, name='barangay-staff-household'),
    path('barangay-staff/add-household/', barangayStaffviews.add_household, name='barangay-staff-add-household'),
    path('barangay-staff/edit-household/<int:pk>/', barangayStaffviews.edit_household, name='barangay-staff-edit-household'),
    path('barangay-staff/pdf/export-household/', ExportHouseholdsPDFView.as_view(), name='barangay-staff-pdf-household'),
    path('barangay-staff/excel/export-household/', ExportHouseholdsExcelView.as_view(), name='barangay-staff-excel-household'),

    path('api/search_heads/', barangayStaffviews.search_residents, name='search_heads'),
    path('api/search_members/', barangayStaffviews.search_residents, name='search_members'),
    path('api/get_household_data/', barangayStaffviews.get_household_data, name='get_household_data'),


    path('barangay-staff/delete-household/<int:pk>/', barangayStaffviews.delete_household, name='barangay-staff-delete-household'),
    path('barangay-staff/resident/', barangayStaffviews.resident, name='barangay-staff-resident'),
    path('barangay-staff/document/', barangayStaffviews.document, name='barangay-staff-document'),
    path('barangay-staff/transactions/', barangayStaffviews.transactions, name='barangay-staff-transactions'),
    path('clearance/edit/<str:clearance_file>/', barangayStaffviews.edit_clearance, name='barangay-staff-edit-clearance'),
    path('indigency/edit/<str:indigency_file>/', barangayStaffviews.edit_indigency, name='barangay-staff-edit-indigency'),
    path('clearance/delete/<str:clearance_file>/', barangayStaffviews.delete_clearance, name='barangay-staff-delete-clearance'),
    path('indigency/delete/<str:indigency_file>/', barangayStaffviews.delete_indigency, name='barangay-staff-delete-indigency'),

    path('barangay-staff/clearance/generate_clearance/<int:resident_id>/', barangayStaffviews.generate_clearance, name='barangay-staff-generate-clearance'),
    path('barangay-staff/indigency/generate_indigency/<int:resident_id>/', barangayStaffviews.generate_indigency, name='barangay-staff-generate-indigency'),
    path('barangay-staff/clearance-pdf/export-residents/', GeneratePDF.as_view(), name='barangay-staff-pdf-export'),
    path('barangay-staff/clearance-excel/export-residents/', GenerateExcel.as_view(), name='barangay-staff-excel-export'),

    path('barangay-staff/logout/', barangayStaffviews.logout, name='barangay-staff-logout'),
    path('barangay-staff/add-resident/', barangayStaffviews.add_resident, name='barangay-staff-add-resident'),
    path('barangay-staff/edit-resident/<int:pk>/', barangayStaffviews.edit_resident, name='barangay-staff-edit-resident'),
    path('barangay-staff/delete-resident/<int:pk>/', barangayStaffviews.delete_resident, name='barangay-staff-delete-resident'),


    path('login/provincial_admin/', views.provincial_admin_login, name='provincial_admin_login'),
    path('login/municipal_admin/', views.home_page, name='municipal_admin_login'),
    path('login/municipal_staff/', views.home_page, name='municipal_staff_login'),
    path('login/barangay_admin/', views.home_page, name='barangay_admin_login'),
    path('login/barangay_staff/', views.home_page, name='barangay_staff_login'),
    path('login/tourist_staff/', views.home_page, name='tourist_staff_login'),



    path('tourist-staff/dashboard/', touristSpotsviews.dashboard, name='tourist-staff-dashboard'),
    path('tourist-staff/tourist-spot/', touristSpotsviews.tourist_spot, name='tourist-staff-tourist-spots'),
    path('tourist-staff/tourist-spot/add-tourist-spot', touristSpotsviews.add_tourist_spot, name='tourist-staff-add-tourist-spot'),
    path('tourist-staff/tourist-spot/edit-tourist-spot/<int:pk>', touristSpotsviews.edit_tourist_spot, name='tourist-staff-edit-tourist-spot'),
    path('tourist-staff/tourist-spot/delete-tourist-spot/<int:pk>/', touristSpotsviews.delete_tourist_spot, name='tourist-staff-delete-tourist-spot'),
    path('tourist-staff/user-settings/', touristSpotsviews.user_settings, name='tourist-staff-user-settings'),
    path('tourist-staff/logout/', touristSpotsviews.logout),



    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)