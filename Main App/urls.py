from django.urls import path
from. import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('', views.home, name  = 'home' ),
    path('user/register',views.register, name= 'register' ),
    path('logout',views.logout,name = 'logout'),
    path('profile', views.profile, name='user-profile'),
    path('profile/update',views.profile_update, name= 'user-profile_update'),
    path('show_bookings',views.show_bookings, name ='show_bookings'),
    path('payment/<int:person_info_id>/<str:slot_start_time>/<str:slot_end_time>/<str:selected_day>', views.payment, name='payment'),
    path('process_payment/<int:person_info_id>/<str:slot_start_time>/<str:slot_end_time>/<str:selected_day>', views.process_payment, name='process_payment'),
    path('add_details/', views.add_details, name='add-details'),
    path('add_LS',views.add_location_service,name = 'add-LS'),
    path('book_slot/<int:person_info_id>/', views.book_slot, name='book-slot'),
    path('delete_booking/<int:id>', views.delete_booking, name = 'delete-booking' ),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
        path('booking_history/<int:person_info_id>/', views.booking_history, name='booking-history'),



path('like/<int:person_info_id>/', views.like, name = 'liked'),

path('feedback/<int:booking_id>', views.feedback),
            path('check/<int:person_info_id>/', views.check, name='check'),




]



urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
