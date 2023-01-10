from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from listings.views import (
    # index,
    prediction,
    CustomLoginView,
    RegisterPage,
    LogoutView,
    predict,
    listing_list, 
    # listing_retrieve, 
    listing_create, 
    listing_update, 
    listing_delete,
    listing_search,
    user_specific_listings,
    LikeView,
    ListingRetrieveView,
    add_comment
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prediction/', prediction, name='prediction'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('prediction/predict', predict, name='predict'),
    path('', listing_list, name='listing_list'),
    path('accounts/', include('allauth.urls')),
    path('listings/<pk>/', ListingRetrieveView.as_view(), name='listing_retrieve'),
    path('user_specific_listings/', user_specific_listings, name='user_specific_listings'),
    path('add-listing', listing_create.as_view(), name='listing_create'),
    path('listings/<pk>/edit/', listing_update.as_view(), name='listing_update'),
    path('listings/<pk>/delete/', listing_delete, name='listing_delete'),
    path('listing_search', listing_search, name='listing_search'),
    path('like/<int:pk>', LikeView, name='like_estate'),
    path('listings/<pk>/comment/', add_comment.as_view(), name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
