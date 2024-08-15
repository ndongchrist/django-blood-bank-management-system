from django.urls import path
from .views import *

urlpatterns = [
    
    #Authentication
    
    path('', home, name='home'),
    path('login/', signin, name='login'),
    path('signin-patient/', register_patient, name='register_patient'),
    path('signin-donor/', register_donor, name='register_donor'),
    path('logout/', signout, name='signout'),
    
    # Dashboard
    path('dashboard', dashboard, name='dashboard'),
    path('make-request', RequestHistoryView.as_view(), name='request_history'),
    path('request-history', MakeRequestView.as_view(), name='make_request'),
    path('delete-request/<str:id>', DeleteRequestView.as_view(), name='delete_request'),
    path('update-request/<str:id>', UpdateRequestView.as_view(), name='update_request'),
    path('create-donation/', CreateDonationView.as_view(), name='create_donation'),
    path('donation-history', DonationHistoryView.as_view(), name='donation_history'),
    path('update-donation/<str:id>', UpdateDonationView.as_view(), name='update_donation'),
    path('delete-donation/<str:id>', DeleteDonationView.as_view(), name='delete_donation'),
    path('all-users/', SuperAdminUserView.as_view(), name='all_users'),
    path('all-donations/', SuperAdminDonationsView.as_view(), name='all_donations'),
    path('all-requests/', SuperAdminRequestView.as_view(), name='all_requests'),
    path('update-request-admin/<str:id>', AdminUpdateRequestView.as_view(), name='update_request_admin'),
    path('update-donate-admin/<str:id>', AdminUpdateDonateView.as_view(), name='update_donate_admin'),
    

]