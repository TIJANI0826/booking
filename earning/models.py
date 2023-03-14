from django.db import models
import os
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from . choice import *
from . utils import code_generator
import uuid
import barcode 
from django.core.files import File 
import qrcode 
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core.validators import RegexValidator


FIRST_NAME_REGEX = RegexValidator(
    regex=r'^[A-Za-z]([a-zA-Z ,\'\.]*)$',
    message="Invalid first name entered"
)
LAST_NAME_REGEX = RegexValidator(
    regex=r'^[a-zA-Z]+$',
    message="Invalid last name entered"
)
PHONE_REGEX = RegexValidator(
    regex=r'^\d{11,11}$',
    message="Please enter a valid phone number. Only 10 digits allowed."
)
ID_NUMBER_REGEX = RegexValidator(
    regex=r'^[a-zA-Z0-9]*$',
    message="Enter a valid id number. Only alphabets and digits allowed."
)

GENDER_CHOICE =[

('Male','Male'),
('Female','Female' )

]

GYM_REASON =[

('Build Body','Build Body'),
('Flat Tommy','Flat Tommy' ),
('Reduce Weight','Reduce Weight'),
('Hips','Hips'),

]

# Create your models here.
class UserManager(BaseUserManager):
    """User Manager for custom User Model"""

    def _create_user(self, email, password, is_superuser, **extra_fields):
        """Save user in db"""

        if not email:
            raise ValueError('Email cannot be blank')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create a user"""

        return self._create_user(
            email,
            password,
            False,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser"""

        return self._create_user(
            email,
            password,
            True,
            **extra_fields
        )

class User(AbstractBaseUser):
    """Custom user model"""
    username = models. CharField(
			max_length=200
    )
    email = models.EmailField(
        'email address',
        unique=True,
    )

    first_name = models.CharField(
        max_length=50,
        null=True,
        validators=[FIRST_NAME_REGEX]
    )

    last_name = models.CharField(
        max_length=50,
        null=True,
        validators=[LAST_NAME_REGEX]
    )

    phone = models.CharField(
        validators=[PHONE_REGEX],
        max_length=13
    )

    address = models.TextField(
        null=True,
    )
    picture	=models.ImageField(
 		verbose_name='Profile Picture',
 		upload_to='photos',
 		null = True,
 		blank=True,
 	)
    timestamp = models.DateTimeField(
    	auto_now=True
    )
    nationality  = models.CharField(
			max_length= 200,
    )
    password = models.CharField(
    	max_length=200
    )
   

    is_admin = models.BooleanField(
        default=False
    )

    is_superuser = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __unicode__(self):
        """unicode method"""
        return '{0} {1} ({2})'.format(self.first_name, self.last_name,
                                      self.email) if self.first_name and self.last_name else self.email

    @property
    def is_staff(self):
        """is staff method"""
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        """has permissions"""
        return True

    def has_module_perms(self, app_label):
        """has module permissions"""
        return True

    def get_short_name(self):
        """get short name"""
        return self.first_name

    def get_full_name(self):
        """get full name"""
        return self.first_name

    def delete_image(self):
        """delete profile image from file system"""
        try:
            os.remove(self.image.path)
        except:
            pass


 	

""" MODEL FOR  BOOKING FOR HALL """	
class Package(models.Model):
    
	name_event	=models.CharField(
		max_length=200
	)
	
	
     
	
	is_approved = models.BooleanField(default=False)
	
	def get_absolute_url(self):
		return reverse('event_details', kwargs={'pk': self.pk})
	def __str__(self):
		return self.name_event
	class Meta():
		verbose_name ="Packages"
		
	
	
#""" MODEL FOR BOOKING TICKET """


    
    
class Members(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name		= models.CharField(
		max_length=200
	)
    phone_number		=models.IntegerField(
		
	)
    gender = models.CharField(
				max_length=30
	)
    date_of_birth	=models.DateTimeField(
		
		verbose_name='Date Of Birth'
	)	
    plan				=models.ForeignKey(
		Package, on_delete=models.CASCADE, 
	)
    reason_for_registering = models.CharField(
        null=True,max_length=100
    )
    start_date	=models.DateTimeField(
		
		verbose_name='Registration Date'
	)
    exp_date	=models.DateTimeField(
		
		verbose_name='Expiring Date'
	)
    barcode	=models.ImageField(
		
		upload_to='barcodes', blank = True
	)
    refered_by  = models.CharField(max_length=200)		
    
    def __str__(self):
        return self.name
	# def save(self, *args, **kwargs):
	# 	qrcode_img = qrcode.make(self.name)
	# 	canvas = Image.new('RGB', (290, 290), 'white')
	# 	draw = ImageDraw.Draw(canvas)
	# 	canvas.paste(qrcode_img)
	# 	frame = f'qr_code-{self.name}'+'.pgn'
	# 	buffer = BytesIO
	# 	canvas.save(buffer, 'PNG')
	# 	self.qrcode.save(fname, File(buffer), save=False)
	# 	canvas.close()
	# 	super().save(*args, **kwargs)
		
	
   # """MODELS FOR GENERATING TICKET NUMBER """
class TicketNumber(models.Model):
	ticket 	=models.ForeignKey(Members, on_delete=models.CASCADE, editable=False)
	ticket_number	=models.CharField(max_length=120, editable=False)
	expired  = models.BooleanField(default=False)
	class Meta():
		verbose_name = 'Ticket Number '
	def get_absolute_url(self):
 		return reverse('ticketdetail', kwargs={'pk': self.pk})
	def save(self, *args, **kwargs):
		self.ticket_number = code_generator()
		super(TicketNumber, self).save(*args, **kwargs)
	def __str__(self):
		return self.ticket.name



#    """MODELS FOR LAUNDRY"""

class Laundry(models.Model):
    customer_name       =models.CharField(max_length=50, verbose_name='Customer Name')
    custom_number       = models.IntegerField(verbose_name='Customer Number')
    shirt               = models.IntegerField(verbose_name='T-Shirt', null = True, blank=True,)
    trouser             = models.IntegerField(verbose_name='Trouser/Short', null = True, blank=True,)
    underwear           = models.IntegerField(verbose_name='Single/Boxers', null = True, blank=True,)
    native              = models.IntegerField(verbose_name='Complete Native', null = True, blank=True,)
    duvet               = models.IntegerField(verbose_name='Duvet', null = True, blank=True,)
    duver_beddings      = models.IntegerField(verbose_name='Duvet and Beddings', null = True, blank=True,)
    towel               = models.IntegerField(verbose_name='Towel', null = True, blank=True,)
    dropp_off           = models.DateTimeField(auto_now=True, null = True, blank=True,)
    commission          = models.CharField(max_length=200, verbose_name='Refered Byss', null = True, blank=True,)

    def __str__(self):
        return self.customer_name

    

    


#""" GENERATE TICKET NUMBER """
def create_ticket(sender, **kwargs):
	if kwargs['created']:
		ticket_number = TicketNumber.objects.create(ticket=kwargs['instance'])
post_save.connect(create_ticket, sender=Members)

#""" GENERATE TICKET NUMBER """

def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
	if created:
		print('activation created ')
post_save.connect(post_save_activation_receiver, sender=TicketNumber)


