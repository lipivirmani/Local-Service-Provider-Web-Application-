from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Count
import random

from .models import Location, Services, Person_info,Booking

from django.contrib.auth.decorators import login_required
from .models import CreateUserForm,UserUpdateForm,ProfileUpdateForm

import random


from .recommendation_system import collaborative_filtering_recommendation, content_based_filtering_new_user
from .recommendation_system import content_based_filtering_recommendation

@login_required
def home(request):
    locations = Location.objects.all()
    services = Services.objects.all()

    if request.method == "POST":
        first = Location.objects.get(location_name=str(request.POST.get('location_name')))
        second = Services.objects.get(service_name=str(request.POST.get('service_name')))
        data = Person_info.objects.filter(location_name=first, service_name=second)

        # Assuming you have a logged-in user
        user = request.user
        user_has_bookings = Booking.objects.filter(user=request.user).exists()
        if user_has_bookings:

        # Collaborative Filtering Recommendations for User with Bookings
            collaborative_filtering_recommendations = collaborative_filtering_recommendation(user)

        # Content-Based Filtering Recommendations for User with Bookings
            content_based_filtering_recommendations = content_based_filtering_recommendation(user)      
            unique_recommendations = []
            for i in collaborative_filtering_recommendations:
                if i.service_name==second and i.location_name == first:
                    unique_recommendations.append(i)
            for j in content_based_filtering_recommendations:
                if j.service_name==second and j.location_name == first:
                    unique_recommendations.append(j)
            
            

            unique_recommendations= list(set(unique_recommendations))

            

            randomly_placed_recommendations = random.sample(unique_recommendations, len(unique_recommendations))
            unique_recommendations=randomly_placed_recommendations


            return render(
                request,
                'test.html',
                {
                    'locations': locations,
                    'services': services,
                    'data': data,
                            'unique_recommendations': unique_recommendations

                }
            )
        else:
            unique_recommendations=[]
            content_based_filtering_new_user_recommendations = content_based_filtering_new_user(second)
            for j1 in content_based_filtering_new_user_recommendations:
                if j1.service_name==second and j1.location_name == first:
                    unique_recommendations.append(j1)
            unique_recommendations= list(set(unique_recommendations))
            if len(unique_recommendations)>=5:
                randomly_placed_recommendations = random.sample(unique_recommendations, 3)
            elif len(unique_recommendations)==1:
                randomly_placed_recommendations = None
            elif len(unique_recommendations)<=3:
                randomly_placed_recommendations = random.sample(unique_recommendations, 1)
            elif len(unique_recommendations)<=4:
                randomly_placed_recommendations = random.sample(unique_recommendations, 2)
   

            unique_recommendations=randomly_placed_recommendations
            content_based_filtering_new_user_recommendations=unique_recommendations

            return render(
                request,
                'test.html',
                {
                    'locations': locations,
                    'services': services,
                    'data': data,
                            'content_based_filtering_new_user_recommendations': content_based_filtering_new_user_recommendations

                }
            )

            

            randomly_placed_recommendations = random.sample(unique_recommendations, 3)
            content_based_filtering_new_user_recommendations=randomly_placed_recommendations
            
            
       


    else:
        # Content-Based Filtering Recommendations for New User (No Bookings)
        content_based_filtering_new_user_recommendations = content_based_filtering_new_user()
        content_based_filtering_new_user_recommendations=list(set(list(content_based_filtering_new_user_recommendations)))
        content_based_filtering_new_user_recommendations=random.sample(content_based_filtering_new_user_recommendations,5)


        return render(
            request,
            'test.html',
            {
                'locations': locations,
                'services': services,
                'content_based_filtering_new_user_recommendations': content_based_filtering_new_user_recommendations,
            }
        )
    



def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered')
            return redirect('/')

    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)


@login_required
def logout(request):
    return render(request,'user/logout_check.html' )


@login_required
def profile(request):
    context = {

    }
    return render(request, 'user/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST': 
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
            }
    return render(request, 'user/profile_update.html', context)



from django.shortcuts import render, get_object_or_404, redirect
# from .models import Person_info, Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from django.contrib import messages


@login_required
def add_details(request):
    locations = Location.objects.all()
    services = Services.objects.all()

    if request.method == 'POST':
        person_name = request.POST.get('person_name')
        person_location_id = request.POST.get('person_location')
        person_service_id = request.POST.get('person_service')
        person_phone = request.POST.get('person_phone')
        person_rate = request.POST.get('person_rate')

        # Assuming you have error handling and validation here

        

        person_location = Location.objects.get(id=person_location_id)
        person_service = Services.objects.get(id=person_service_id)

        person_info = Person_info.objects.create(
            name=person_name,
            location_name=person_location,
            service_name=person_service,
            Phone_No=person_phone,
            Per_hour_rateINR=person_rate,
        )
        messages.success(request, 'Details added successfully!')
    return render(request, 'add_details.html', {'locations': locations, 'services': services})


@login_required
def add_location_service(request):
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        service_name = request.POST.get('service_name')
        if len(location_name)==0 and len(service_name)==0:
                return redirect('/add_details/')
        if len(location_name)!=0:
            location = Location.objects.create(location_name=location_name)
        if len(service_name)!=0:
            service = Services.objects.create(service_name=service_name)
        messages.success(request, 'Details added successfully!')
        return redirect('/add_details/')



@login_required
def book_slot(request, person_info_id):
    person_info = Person_info.objects.get(pk=person_info_id)
    user = request.user

    a = Booking.objects.filter(person_info=person_info)
    if request.method == 'POST':
            slot_start_time = request.POST.get('slot_start_time')
            slot_end_time = request.POST.get('slot_end_time')
            selected_day = request.POST.get('selected_day')
            try:
                a=Booking.objects.create(
                    person_info=person_info,
                    user= request.user,
                    slot_start_time=slot_start_time,
                    slot_end_time=slot_end_time,
                    selected_day=selected_day
                )
                a.delete()
                return redirect(f'/payment/{person_info_id}/{slot_start_time}/{slot_end_time}/{selected_day}')
            except:
                messages.error(request,"Slot already booked ")




    return render(request, 'booking_slot.html', { 'person_info': person_info, 'data': a})


def check(request,person_info_id ):
    person_info = Person_info.objects.get(pk=person_info_id)
    user = request.user
    existing_booking = Booking.objects.filter(user=user, person_info=person_info)
    aa=existing_booking
    if len(existing_booking)!=0:
        return redirect(f'/feedback/{aa.last().id}')
    else:
        return redirect(f'/book_slot/{person_info.id}/')





def feedback(request, booking_id):
    booking=Booking.objects.get(id=booking_id)
    messages.success(request, 'Thanks for giving feedback')
    return render(request, 'feedback.html', {'booking':booking})



@login_required
def show_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'show_bookings.html', {'user_bookings': user_bookings})


@login_required
def delete_booking(request,id):
    if request.method=="POST":
        id=int(id)
        a= Booking.objects.get(id=id)
        a.delete()
        return redirect('/show_bookings')
    
from datetime import datetime, timedelta

def calculate_total_hours(time_a, time_b):
    # Parse time strings into datetime objects
    datetime_a = datetime.strptime(time_a, "%H:%M")
    datetime_b = datetime.strptime(time_b, "%H:%M")

    # Check if time_b is on the next day
    if datetime_b < datetime_a:
        datetime_b += timedelta(days=1)

    # Calculate the time difference
    time_difference = datetime_b - datetime_a

    # Convert the time difference to total hours
    total_hours = time_difference.total_seconds() / 3600

    return total_hours

# Example usage
# a = '11:00'
# b = '23:00'

# total_hours = calculate_total_hours(a, b)

# total_hours= int(total_hours)


@login_required
def payment(request,person_info_id,slot_start_time,slot_end_time,selected_day):
    person_info = Person_info.objects.get(pk=person_info_id)
    # aa=Booking.objects.create(
    #                 person_info=person_info,
    #                 user=request.user,
    #                 slot_start_time=slot_start_time,
    #                 slot_end_time=slot_end_time,
    #                 selected_day=selected_day
    #             )
    
    # id = aa.pk
    # a=Booking.objects.get(id=id)
    total = int(person_info.Per_hour_rateINR)
    b= str(slot_start_time)
    b1=str(slot_end_time)
    total_hours = int(abs(int(calculate_total_hours(b, b1))))
    total_amount = total* total_hours
    return render(request, 'payment.html', {'person_info':person_info, 'total_amount': total_amount, 'slot_start_time':slot_start_time, 'slot_end_time':slot_end_time, 'selected_day':selected_day }  )
    #return HttpResponse("Booking Done <br> Check in your Booking : <a href = '/show_bookings' >Booking</a> ")  # Replace 'booking_success' with your success page



@login_required
def process_payment(request,person_info_id,slot_start_time,slot_end_time,selected_day):
    if request.method == 'POST':
        person_info = Person_info.objects.get(pk=person_info_id)
        person_info.likes+=1
        person_info.save()
        Booking.objects.create(
                    person_info=person_info,
                    user=request.user,
                    slot_start_time=slot_start_time,
                    slot_end_time=slot_end_time,
                    selected_day=selected_day
                )


        # Handle payment processing logic here
        # This is a placeholder, you should integrate with a payment gateway
        # and handle actual payment processing, update booking status, etc.

        # For demonstration purposes, let's assume the payment was successful
        return render(request, 'booking_success.html')
    else:
        return HttpResponse('Invalid request method')
    



# views.py

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import PasswordResetToken


def password_reset_request(request):
    if request.method == "POST":
        email= request.POST.get('email')
        

        try:
            user = User.objects.get( email=email)
        except User.DoesNotExist:
            # Handle non-existent user
            return render(request, 'password_reset_request.html', {'error': 'User not found'})

        # Generate a unique token
        token = default_token_generator.make_token(user)

        # Save the token in the database
        PasswordResetToken.objects.update_or_create(user=user, defaults={'token': token})

        # Redirect to a page with the token
        token=str(token)
        return redirect(f'/password_reset_confirm/{token}')

    return render(request, 'password_reset_request.html')


# views.py

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import PasswordResetToken
from django.contrib import messages

def password_reset_confirm(request, token):
    token_record = get_object_or_404(PasswordResetToken, token=token)
    user = token_record.user

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset successfully. You can now log in with your new password.')
            return redirect('/')
    else:
        form = SetPasswordForm(user)

    return render(request, 'password_reset_confirm.html', {'form': form})




def booking_history(request,person_info_id):
    person_info=Person_info.objects.get(id=person_info_id)
    data = Booking.objects.filter(person_info=person_info)
    return render(request, 'booking_history.html' ,{'data' : data, 'person_info':person_info} )


def like(request, person_info_id):
    if request.method == 'POST':
        person_info = Person_info.objects.get(id=person_info_id)
        user = request.user

        # Check if the user has already liked this person
        if user in person_info.liked_users.all() or user in person_info.disliked_users.all():
            messages.warning(request, "You have already liked or disliked  this person.")
        else:
            person_info.likes += 1
            person_info.liked_users.add(user)
            person_info.save()
            messages.success(request, "Liked")

    return redirect('show_bookings')
