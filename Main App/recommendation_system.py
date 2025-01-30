# Import necessary libraries
from sklearn.metrics.pairwise import cosine_similarity
from .models import Person_info,Booking
import numpy as np

# Assuming you have a list of all users with bookings and their corresponding information
all_users_with_bookings = Person_info.objects.filter(booking__isnull=False).distinct()
# Function to get recommendations for a user based on collaborative filtering
def collaborative_filtering_recommendation(user):
    # Extract features for collaborative filtering
    booked_person_info = Person_info.objects.filter(booking__user=user).distinct()
    # Extract features for collaborative filtering from the booked Person_info objects
    features = ['likes', 'rating',  'Per_hour_rateINR']
    booked_person_info_data = booked_person_info.values(*features)
    user_data=booked_person_info_data
    user_data = list(booked_person_info_data)


    # Create a matrix with users and their features
    users_matrix = []
    for u in all_users_with_bookings:
        user_vector = [getattr(u, feature, 0) for feature in features]
        users_matrix.append(user_vector)

    # Calculate cosine similarity
    users_matrix = np.array(users_matrix)

    # Convert the user_data to a NumPy array
    user_data = np.array([[user_dict[feature] for feature in features] for user_dict in user_data])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(user_data, users_matrix)


    # Get indices of top 4 similar users
    top_indices = np.argsort(similarity_matrix[0]).tolist()

    # Get recommendations based on similar users
    recommendations = Person_info.objects.filter(id__in=[all_users_with_bookings[i].id for i in top_indices])

    return recommendations





# Function to get recommendations for a user based on content-based filtering
def content_based_filtering_recommendation(user):
    # Extract features for content-based filtering
    features = [ 'likes', 'rating', 'Per_hour_rateINR']

    # Get booked persons by the user
    aa=Booking.objects.filter(user=user)

    booked_persons = aa.values_list('person_info__id', flat=True)

    # Get persons not booked by the user
    not_booked_persons = Person_info.objects.exclude(id__in=booked_persons)

    # Calculate a content similarity score
    content_similarity_scores = []
    for person in not_booked_persons:
        content_vector = [person.__dict__[feature] for feature in features]
        uu=Person_info.objects.get(id = person.id)
        user_vector = [uu.__dict__[feature] for feature in features]
        similarity_score = cosine_similarity([content_vector], [user_vector])[0][0]
        content_similarity_scores.append((person, similarity_score))

    # Get top 4 recommendations based on content similarity
    recommendations = [recommendation[0] for recommendation in sorted(content_similarity_scores, key=lambda x: x[1], reverse=True)[:5]]

    return recommendations


# Function to get recommendations for a new user based on content-based filtering
def content_based_filtering_new_user(second=0):
    # Extract features for content-based filtering
    if second==0:
        features = [ 'likes']

        # Get all persons
        all_persons = Person_info.objects.all()

        # Calculate a content similarity score
        content_similarity_scores = []
        for person in all_persons:
            content_vector = [person.__dict__[feature] for feature in features]
            new_user_vector = [0]  # Assuming a new user has no ratings yet
            similarity_score = cosine_similarity([content_vector], [new_user_vector])[0][0]
            content_similarity_scores.append((person, similarity_score))

        # Get top 4 recommendations based on content similarity
        recommendations = [recommendation[0] for recommendation in sorted(content_similarity_scores, key=lambda x: x[1], reverse=True)]

        return recommendations
    else:
        features = [ 'likes']

        # Get all persons
        all_persons = Person_info.objects.filter(service_name = second)

        # Calculate a content similarity score
        content_similarity_scores = []
        for person in all_persons:
            content_vector = [person.__dict__[feature] for feature in features]
            new_user_vector = [0]  # Assuming a new user has no ratings yet
            similarity_score = cosine_similarity([content_vector], [new_user_vector])[0][0]
            content_similarity_scores.append((person, similarity_score))

        # Get top 4 recommendations based on content similarity
        recommendations = [recommendation[0] for recommendation in sorted(content_similarity_scores, key=lambda x: x[1], reverse=True)]

        return recommendations




