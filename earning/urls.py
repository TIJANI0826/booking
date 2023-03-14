from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.views import login
from earning.views import *
from earning import views

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),   
    url(r'^signup/$', UserRegistration.as_view(), name='user_registration'),
    url(r'^login/$',LoginFormView.as_view(),name='login'),
    url(
        r'^profile/$',
            ProfileView.as_view(),
        
        name="profile"
    ),
    url(r'^editprofile/(?P<pk>\d+)/update$',UpdateProfile.as_view(),name='editprofile'),
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
    url(
        r'^halls/$',
        
            HallView.as_view(),
        
        name="halls"
    ),
    url(
        r'^booking/(?P<hall_pk>[\d]+)/$',
        
            HallBookingView.as_view(),
            name='new-booking'
        ),
    url(
        r'^events/$',
        
            EventView.as_view(),
        
        name="events"
    ),
    url(
        r'^event/(?P<pk>[\d]+)/$',
        
            EventDetails.as_view(),
            name='event_details'
        ),
   
    url(
        r'^tickets/$',
        
            TicketDetails.as_view(),
        
        name="edit_ticket_list"
    ),

    url(
        r'^tickets/(?P<pk>[\d]+)$',
        
            EditTicketDetails.as_view(),      
            name='edit_ticket'
    ),
    
    
#    MEMBER REGISTRATIOn
    
    url(
        r'^member/add/$',
        
            RegMemberView.as_view(),
    
        name="add_member"
    ),
    
    url(
        r'^event/(?P<pk>[\d]+)/$',
        
            MemberDetails.as_view(),
            name='member_details'
        ),

# LAUNDRY

url(
        r'^laundry/add/$',
        
            LaundryReg.as_view(),
    
        name="laundry"
    ),
    
url(
        r'^laundries/$',
        
            LaundryDetails.as_view(),
        
        name="laundrys"
    ),

]
