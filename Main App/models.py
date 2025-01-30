from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Location(models.Model):
    location_name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.location_name

class Services(models.Model):
    service_name = models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.service_name
    

class Person_info(models.Model):
    name = models.CharField(max_length=150)
    location_name = models.ForeignKey(Location, on_delete=models.CASCADE)
    service_name = models.ForeignKey(Services, on_delete=models.CASCADE)
    Phone_No = models.CharField(max_length=20)
    Per_hour_rateINR = models.PositiveIntegerField(default=500)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_persons', blank=True)
    disliked_users = models.ManyToManyField(User, related_name='disliked_persons', blank=True)
    rating = models.FloatField(default=0)  # Assuming you want to store ratings as floats
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)


    class Meta:
        verbose_name = "Person Info"
        verbose_name_plural = "Person Info"

  

    def calculate_rating(self):
        total_likes = self.likes
        total_bookings = Booking.objects.filter(person_info=self).count()
        avg_rating = self.avg_rating  # Use the stored average rating

        # Your adjusted formula, considering both average rating and total bookings
        rating = max((avg_rating + total_bookings * 0.2) / 10, 1)  # Adjust weights as needed
        # Ensure that the rating is within a certain range (e.g., 0 to 5 stars)
        rating = max(min(rating, 5), 0)
        return rating


    class Meta:
        verbose_name = "Person Info"
        verbose_name_plural = "Person Info"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Update the average rating field before saving
        bookings = Booking.objects.filter(person_info=self)
        if bookings.exists():
            total_ratings = sum(booking.feedback_rating for booking in bookings)
            self.avg_rating = total_ratings / len(bookings)
        else:
            self.avg_rating = 0.0
        self.rating = self.calculate_rating()


        super().save(*args, **kwargs)







class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True, default='N/A'  )
    phone = models.CharField(max_length=50, null=True,default='N/A')
    image = models.ImageField(default='default.png',
                              upload_to='profile_images')

    def __str__(self):
        return f'{self.name.username}-Profile'



from .models import Profile


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']





from django.utils import timezone



class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token for {self.user.username}"
    
from django.core.exceptions import ValidationError



from django.db.models import F, Q
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User



class Booking(models.Model):
    person_info = models.ForeignKey(Person_info, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot_start_time = models.TimeField()
    slot_end_time = models.TimeField()
    selected_day = models.DateField()
    FEEDBACK_CHOICES = [
        (0,'0 star'),
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    feedback_rating = models.PositiveIntegerField(
        choices=FEEDBACK_CHOICES,
        default=0,  # You can set a default value if needed
    )

    def clean(self):
        # Check for overlapping time slots for the same person on the same day
        overlapping_records = Booking.objects.filter(
            person_info=self.person_info,
            selected_day=self.selected_day,
            slot_start_time__lt=self.slot_end_time,
            slot_end_time__gt=self.slot_start_time,
        )

        if overlapping_records.exists():
            raise ValidationError("This time slot is already booked for the selected day.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run full validation before saving
        super().save(*args, **kwargs)
        
        # Update the average rating for associated Person_info
        self.person_info.save()
    
    

