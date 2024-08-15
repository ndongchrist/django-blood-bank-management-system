import logging


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Request, User
from django.contrib.auth.hashers import make_password
from .models import BloodTypes
from global_data.enums import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'index.html')



def register_patient(request):
    context = {}
    if request.method == 'POST':
        # Retrieve and validate form data
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        blood_group = request.POST.get('blood_group')
        illness = request.POST.get('illness')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')


        try:
            if password1 != password2:
                return render(request, 'accounts/singup_patient.html', {'message': 'Passwords do not match'})

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'accounts/singup_patient.html', {'message': 'Email already registered'})
            
            # Check if email already exists
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/singup_patient.html', {'message': 'Username already registered'})


            # Create a new user
            user = User.objects.create(
                username=username, 
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                gender=gender,
                age=age,
                weight=weight,
                blood_group=blood_group,
                user_type = UserTypes.PATIENT,
                password=make_password(password1)  # hash password
            )
            user.save()
            context['message'] = 'Operation Successfull'
        except Exception as e:
            context['message'] = 'Sorry an error occured'
            logger.error(e)
        
        # Redirect to a success page or login page
        return redirect('login')  # or any other page

    # GET request or invalid POST request

    return render(request, 'accounts/singup_patient.html', context)


def register_donor(request):
    context={}
    if request.method == 'POST':
        # Retrieve and validate form data
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        blood_group = request.POST.get('blood_group')
        illness = request.POST.get('illness')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        
        try:
            if password1 != password2:
                return redirect('register_donor')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return redirect('register_donor')

            # Create a new user
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                gender=gender,
                age=age,
                weight=weight,
                blood_group=blood_group,
                user_type = UserTypes.DONOR,
                password=make_password(password1)  # hash password
            )
            user.save()
            context['message'] = 'Operation Successfull'
        except Exception as e:
            context['message'] = 'Sorry an error occured'
            logger.error(e)
        # Redirect to a success page or login page
        return redirect('login')  # or any other page

    # GET request or invalid POST request
    return render(request, 'accounts/signup_donor.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')  # Redirect to the home page or wherever you want
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    context = {}
    if request.user.user_type == UserTypes.PATIENT:
        your_requests = Request.objects.filter(user_requesting=request.user)
        accepted_request = Request.objects.filter(user_requesting=request.user,status=Status.COMPLETED)
        rejected_request = Request.objects.filter(user_requesting=request.user,status=Status.CANCELLED)
        peding_request = Request.objects.filter(user_requesting=request.user,status=Status.PENDING)
        context['request_number'] = your_requests.count() or 0
        context['accepted_number'] = accepted_request.count() or 0
        context['rejected_request'] = rejected_request.count() or 0
        context['pending_request'] = peding_request.count() or 0
        
    elif request.user.user_type == UserTypes.DONOR:
        donations = Donation.objects.filter(donor=request.user)
        accepted_donations = Donation.objects.filter(donor=request.user,status=Status.COMPLETED)
        rejected_donations = Donation.objects.filter(donor=request.user,status=Status.CANCELLED)
        pending_donations = Donation.objects.filter(donor=request.user,status=Status.PENDING)
        context['donations'] = donations.count() or 0
        context['accepted_donations'] = accepted_donations.count() or 0
        context['rejected_donations'] = rejected_donations.count() or 0
        context['pneding_donations'] = pending_donations.count() or 0
        
    elif request.user.is_superuser:
        donations = Donation.objects.all()
        users = User.objects.all()
        requests = Request.objects.all()
        
        #request stats
        accepted_request = Request.objects.filter(status=Status.COMPLETED)
        rejected_request = Request.objects.filter(status=Status.CANCELLED)
        peding_request = Request.objects.filter(status=Status.PENDING)
        
        #donation stats
        accepted_donations = Donation.objects.filter(status=Status.COMPLETED)
        rejected_donations = Donation.objects.filter(status=Status.CANCELLED)
        pending_donations = Donation.objects.filter(status=Status.PENDING)
        
        #all donors and patients
        donors = User.objects.filter(user_type =  UserTypes.DONOR)
        patients = User.objects.filter(user_type =  UserTypes.PATIENT)
        
        context['donations'] = donations.count() or 0
        context['users'] = users.count() or 0
        context['requests'] = requests.count() or 0
        
        context['donors'] = donors.count() or 0
        context['patients'] = patients.count() or 0
        
        
        context['accepted_number'] = accepted_request.count() or 0
        context['rejected_request'] = rejected_request.count() or 0
        context['pending_request'] = peding_request.count() or 0
        
        context['accepted_donations'] = accepted_donations.count() or 0
        context['rejected_donations'] = rejected_donations.count() or 0
        context['pneding_donations'] = pending_donations.count() or 0
   
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def signout(request):
    logout(request)
    return render(request, 'index.html')


class RequestHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        your_requests = Request.objects.filter(user_requesting=request.user)
        context = {
            'your_requests':your_requests,
        }
        print(your_requests)
        return render(request, 'dashboard/request_history.html', context)
    
class MakeRequestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/make_request.html')

    def post(self, request, *args, **kwargs):
        volume = request.POST.get('volume')
        blood_group = request.POST.get('blood_group')
        date = request.POST.get('date')
        description = request.POST.get('description')

        if not all([volume, blood_group, date, description]):
            messages.error(request, "All fields are required.")
            return redirect('make_request')

        try:
            new_request = Request.objects.create(
                user_requesting=request.user,
                volume=volume,
                blood_group=blood_group,
                date=date,
                notes=description
            )
            new_request.save()
            messages.success(request, "Request made successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('make_request')

        return redirect('request_history')
    
    
class DeleteRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        
        
        
        #get the user request
        my_request = Request.objects.filter(id=request_id)
        my_request.delete()
        messages.success(request, 'Request Deleted')
        logger.info('REQUEST DELETED')
        return redirect('request_history')
    
class UpdateRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        my_request = Request.objects.filter(id=request_id).first()
        
        print(my_request)
        
        volume = request.POST.get('volume')
        blood_group = request.POST.get('blood_group')
        date = request.POST.get('date')
        description = request.POST.get('description')
        try:
            my_request.volume = volume
            my_request.date = date
            my_request.notes = description
            my_request.blood_group = blood_group
            my_request.save()
            
            messages.success(request, "Request Updated successfully")
            logger.info()
        except Exception as E:
            messages.error(request, "An Error Occured during update")
            
        return redirect('request_history')
    
class CreateDonationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):       
        return render(request, 'dashboard/make_donation.html')
    
    def post(self, request, *args, **kwargs):
        volume = request.POST.get('volume')
        blood_group = request.POST.get('blood_group')
        date = request.POST.get('date')
        notes = request.POST.get('notes')

        # Create a new Donation object
        donation = Donation.objects.create(
            donor=request.user,
            volume=volume,
            blood_group=blood_group,
            date=date,
            notes=notes
        )
        donation.save()
        # Display a success message
        messages.success(request, "Donation created successfully.")

        # Redirect to the view where donations are listed
        return redirect('donation_history') 
    
class DonationHistoryView(LoginRequiredMixin, View):
   def get(self, request, *args, **kwargs):
        your_donation = Donation.objects.filter(donor=request.user)
        context = {
            'your_donation':your_donation,
        }
        print(your_donation)
        return render(request, 'dashboard/donation_history.html', context)
    
class UpdateDonationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Get the donation object by its ID
        try:
            donation_id = kwargs.get('id')
            donation = Donation.objects.filter(id=donation_id).first()
            
            # Update the donation object with new data from the form
            donation.volume = request.POST.get('volume')
            donation.blood_group = request.POST.get('blood_group')
            donation.date = request.POST.get('date')
            donation.notes = request.POST.get('notes')
            
            # Save the updated donation object
            donation.save()

            # Add a success message
            messages.success(request, 'Donation updated successfully.')
        except Exception as e:
            messages.error(request, 'Donation Update failed')
        
        # Redirect to the list view or another appropriate view
        return redirect('donation_history')
        

class DeleteDonationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Get the donation object by its ID
        donation_id = kwargs.get('id')
        donation = Donation.objects.filter(id=donation_id).first()
        
        # Delete the donation object
        donation.delete()

        # Add a success message
        messages.success(request, 'Donation deleted successfully.')
        
        # Redirect to the list view or another appropriate view
        return redirect('donation_history')
    
    
class SuperAdminUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        context = {
            'users': users
        }
        return render(request, 'dashboard/superuser/all_users.html', context)
    
class SuperAdminDonationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        total_volume = Donation.objects.aggregate(Sum('volume'))['volume__sum']
        context = {
            'donations': donations,
            'total_volume':total_volume, 
        }
        return render(request, 'dashboard/superuser/all_donations.html', context)
    
class SuperAdminRequestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        requests = Request.objects.all()
        total_volume = Request.objects.aggregate(Sum('volume'))['volume__sum']
        context = {
            'requests': requests,
            'total_volume':total_volume,
        }
        return render(request, 'dashboard/superuser/all_request.html', context)
    
class AdminUpdateRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #get the request id
        request_id = kwargs.get('id')
        try:
            current_request = Request.objects.filter(id=request_id).first()
        
            #get the status
            status = request.POST.get('status')
            
            current_request.status = status
            current_request.save()
        except Exception as e:
            messages.error('An Error Occured while Updating Request')
        
        
        return redirect('all_requests')
        
        
class AdminUpdateDonateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        #get the request id
        donation_id = kwargs.get('id')
        try:
            donation = Donation.objects.filter(id=donation_id).first()
        
            #get the status
            status = request.POST.get('status')
            
            donation.status = status
            donation.save()
        except Exception as e:
            messages.error('An Error Occured while Updating Donation')
        
        
        return redirect('all_donations')