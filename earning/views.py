from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (
    CreateView, 
    DetailView, 
    TemplateView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    RedirectView)
from . forms import *
from . models import *

from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy, resolve
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)


LOGIN_SUCCESS_MESSAGE = 'You Have SuccesFully Login'
LOGOUT_SUCCESS_MESSAGE = 'You Have SuccesFully Logout'
LOGIN_INVALID_MESSAGE = 'Invalid login'

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        halls = Package.objects.filter()
        ctx['halls'] = halls

        return ctx


class UserRegistration(CreateView):
	form_class = UserRegistration
	success_url = reverse_lazy("login")
	template_name = 'user_registration.html'


class LoginFormView(FormView):
    """
    View for login page
    """
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        If form is valid, authenticate user
        """
        # Initialize credentials for authentication
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember = form.cleaned_data['remember']

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        # If authentication passed, send to dashboard
        return self.authenticate_user(user, remember) if user else self.credentials_error(form)

    def authenticate_user(self, user, remember=False):
        """
        Function to authenticate a user
        """
        auth.login(self.request, user)
        messages.success(self.request, LOGIN_SUCCESS_MESSAGE)

        if not remember:
            self.request.session.set_expiry(0)

        if self.request.GET.get('next'):
            return HttpResponseRedirect(self.request.GET['next'])
        else:
            return HttpResponseRedirect(self.get_success_url())

    def credentials_error(self, form):
        """
        Function to give error if wrong credentials entered
        """
        messages.warning(self.request, LOGIN_INVALID_MESSAGE)
        return super(LoginFormView, self).form_invalid(form)


class LogoutView(RedirectView):
    """
    View for logout
    """
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        """
        Processing get request to log a user out
        """
        url = self.get_redirect_url(*args, **kwargs)

        # If user was authenticated, log out
        logout(request)
        messages.success(request, LOGOUT_SUCCESS_MESSAGE)
        return redirect('login')

class ProfileView(DetailView):
    """
    View for profile page
    """
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        """
        Fetching user profile for viewing
        """
        obj = User.objects.get(id=self.request.user.id)
        return obj


class UpdateProfile(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_registration.html'
    success_url = reverse_lazy("login")

""" CRETAE HALL"""

class HallView(TemplateView):
    template_name = 'hall/reservation.html'

    def get_context_data(self, **kwargs):
        ctx = super(HallView, self).get_context_data(**kwargs)

        halls = Hall.objects.filter(availability=True)
        ctx['halls'] = halls

        return ctx




"""VIEWS FOR REGISTERIG AN OCCASSION """
class HallBookingView(CreateView):
    form_class = HallBooking
    template_name = 'hall/bookhall.html'

    def get_halls(self):
        hall_pk = self.kwargs['hall_pk']
        halls = Hall.objects.get(pk=hall_pk)

        return halls

    def get_context_data(self, **kwargs):
        ctx = super(HallBookingView, self).get_context_data(**kwargs)
        ctx['halls'] = self.get_halls()

        return ctx

    def form_valid(self, form):
        new_booking = form.save(commit=False)
        new_booking.hall = self.get_halls()
        

        new_booking.save()

        return super(HallBookingView, self).form_valid(form)

    def get_success_url(self):
        hall = self.get_halls()
        hall_details_page_url = hall.get_absolute_url()

        return '{}?booking-success=1'.format(hall_details_page_url)


""" TICKET VIEW"""


class EventView(TemplateView):
    template_name = 'event/events.html'

    def get_context_data(self, **kwargs):
        ctx = super(EventView, self).get_context_data(**kwargs)

        tickets = Package.objects.all()
        ctx['tickets'] = tickets

        return ctx


class EventDetails(DetailView):
    template_name = 'event/eventsdetails.html'
    model = Package

    def get_context_data(self, **kwargs):
        ctx = super(EventDetails, self).get_context_data(**kwargs)
        ctx['booking_success'] = 'booking-success' in self.request.GET

        return ctx


#REGISTERING MEMBERS    

class RegMemberView(CreateView):
    form_class = RegMember
    template_name = 'member/regmember.html'
    success_url = reverse_lazy("edit_ticket_list")
	
#Member Details

    
class MemberDetails(TemplateView):
    template_name = 'member/memberdetail.html'

    def get_context_data(self, **kwargs):
        ctx = super(MemberDetails, self).get_context_data(**kwargs)

        tickets = TicketNumber.objects.filter(expired=False)
        ctx['tickets'] = tickets
        return ctx
    
    
# LAUNDRY

class LaundryReg(CreateView):
    form_class = RegLaundry
    template_name = 'laundry/laundreg.html'
    success_url = reverse_lazy("laundrys")
	
#Member Details


class LaundryDetails(ListView):
    model = Laundry
    context_object_name = 'laundries'
    template_name = 'laundry/laundrydetail.html'


    









class TicketDetails(TemplateView):
    template_name = 'ticket/ticketsdetail.html'

    def get_context_data(self, **kwargs):
        ctx = super(TicketDetails, self).get_context_data(**kwargs)

        tickets = TicketNumber.objects.filter(expired=False)
        ctx['tickets'] = tickets
        return ctx

class EditTicketDetails(UpdateView):
    """
    View for ticket editing
    """

    model = TicketNumber
    template_name = 'ticket/edit_ticket.html'
    form_class = EditBookedTicket
    success_url = reverse_lazy('edit_ticket_list')

    def form_valid(self, form):
        """
        Adding message when item is updated
        """
        if form.has_changed():
            messages.success(
                self.request,
                "This Ticket Has Been Used"
            )

            return super(EditTicketDetails, self).form_valid(form)

        return HttpResponseRedirect(self.get_success_url())


