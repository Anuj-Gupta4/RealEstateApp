from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Listing, Comment, ListingImage
from .forms import ListingForm, CommentForm, SignUpForm, EmailForm
import pandas as pd
import joblib
from django.core.mail import send_mail
from django.contrib import messages

#load the machine learning model
reloadModel = joblib.load('./models/pipeline.pkl')

# Create your views here.
class CustomLoginView(LoginView):
    template_name='login.html'
    fields = '__all___'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('listing_list')

class RegisterPage(FormView):
    template_name='register.html'
    form_class = SignUpForm
    redirect_authenticated_user=True
    success_url = reverse_lazy('listing_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('listing_list')
        return super(RegisterPage, self).get(*args, **kwargs)

def prediction(request):
    temp={}
    context= {'temp':temp}
    return render(request, 'base.html',context)

def predict(request):
    print(request)
    if request.method == 'POST':
            
        temp=dict()
        # temp.columns =['Name', 'Code', 'Age', 'Weight']
        temp['City'] = [request.POST.get('City')]
        temp['Address'] = [request.POST.get('Address')]
        temp['Bedroom'] = [request.POST.get('Bedroom')]
        temp['Bathroom'] = [request.POST.get('Bathroom')]
        temp['Floors'] = [request.POST.get('Floors')]
        temp['Parking'] = [request.POST.get('Parking')]
        temp['Year'] = [request.POST.get('Year')]
        temp['Face'] = [request.POST.get('Face')]
        temp['Area'] = [request.POST.get('Area')]
        temp['Road_Width'] = [request.POST.get('Road_Width')]
        temp['Road_Type'] = [request.POST.get('Road_Type')]
        temp['Build_Area'] = [request.POST.get('Build_Area')]
        temp['Amenities'] = [request.POST.get('Amenities')]
        print(temp)

    data_df = pd.DataFrame(temp)
    ans= int(reloadModel.predict(data_df))

    context={'scoreval':ans,'temp':temp}
    return render(request,'base.html',context)

# @login_required
def listing_list(request):
    listings = Listing.objects.all()
    context = {
        "listings" : listings
    }
    return render(request, "listings.html", context)

#CRUD -Create, Retrieve, Update, Delete
class listing_create(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    # fields= ['Title', 'Location', 'City', 'Price', 'Bedroom', 'Bathroom', 'Floors', 'Parking', 'Face', 'Area', 'Road_Width', 
    # 'Road_Type', 'Build_Area', 'Amenities', 'Contact_number', 'Contact_mail', 'Image']
    template_name='listing_create.html'
    success_url=reverse_lazy('user_specific_listings')

    def form_valid(self,form):
        form.instance.user=self.request.user
        # Get the images from the request
        images = self.request.FILES.getlist('Image')

        # Save the form and create a new instance of the Listing model
        response = super().form_valid(form)

        # Process the images and associate them with the listing
        for image in images:
            print(image)
            ListingImage.objects.create(listing=self.object, image=image)
        return response

class ListingRetrieveView(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'listing.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["liked"] = liked
        context['images'] = ListingImage.objects.filter(listing=self.object)
        context['form'] = EmailForm()
        return context

    def post(self, request, *args, **kwargs):
        listing = self.get_object()
        slug = listing.slug
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'anujgupta.4388@gmail.com'
            recipient_list = [listing.Contact_mail]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Mail sent successfully!')
            return HttpResponseRedirect(reverse('listing_retrieve', args=[str(slug)]))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class listing_update(LoginRequiredMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listing_update.html'
    success_url = reverse_lazy('user_specific_listings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Get the images from the request
        images = self.request.FILES.getlist('Image')

        # Save the form and update the instance of the Listing model
        response = super().form_valid(form)

        # Process the images and associate them with the listing
        ListingImage.objects.filter(listing=self.object).delete()
        for image in images:
            ListingImage.objects.create(listing=self.object, image=image)

        return response

@login_required
def listing_delete(request, pk):
    listing = Listing.objects.get(id = pk)
    listing.delete()
    return redirect("/user_specific_listings")

@login_required
def user_specific_listings(request):
    queryset_list=Listing.objects.all()
    username = request.user.username
    queryset_list=Listing.objects.filter(user__username=username)

    context={
        'listings':queryset_list,
    }

    return render(request, "user_specific_listings.html", context)

# @login_required
def listing_search(request):
    queryset_list=Listing.objects.all()
    # val = False

    # Title
    if 'Title' in request.GET:
        Title = request.GET['Title']
        if Title:
            queryset_list = queryset_list.filter(Title__icontains = Title)
    else:
        Title = ''
        
    #City
    if 'City' in request.GET:
        city = request.GET['City']
        if city:
            queryset_list=queryset_list.filter(City__iexact = city)
    else:
        city = ''

    #Face
    if 'Face' in request.GET:
        Face = request.GET['Face']
        if Face:
            queryset_list=queryset_list.filter(Face__iexact = Face)
    else:
        Face = ''
    
     # Bedroom
    if 'Bedroom' in request.GET:
        Bedroom = request.GET['Bedroom']
        if Bedroom:
            queryset_list=queryset_list.filter(Bedroom__gte=Bedroom)
    else:
        Bedroom = ''

    # Bathroom
    if 'Bathroom' in request.GET:
        Bathroom = request.GET['Bathroom']
        if Bathroom:
            queryset_list=queryset_list.filter(Bathroom__gte=Bathroom)
    else:
        Bathroom = ''

    # Floors
    if 'Floors' in request.GET:
        Floors = request.GET['Floors']
        if Floors:
            queryset_list=queryset_list.filter(Floors__gte=Floors)
    else:
        Floors = ''

    # Area
    if 'Area' in request.GET:
        Area = request.GET['Area']
        if Area:
            queryset_list=queryset_list.filter(Area__lte=Area)
    else:
        Area = ''

    # Price
    if 'Min_Price' in request.GET:
        Min_Price = request.GET['Min_Price']
        if Min_Price:
            queryset_list=queryset_list.filter(Price__gte=Min_Price)
    else:
        Min_Price = ''

    if 'Max_Price' in request.GET:
        Max_Price = request.GET['Max_Price']
        if Max_Price:
            queryset_list=queryset_list.filter(Price__lte=Max_Price)
    else:
        Max_Price = ''

    #show on sale only
    # if 'is_sold' in request.GET:
    #     is_sold = request.GET['is_sold']
    #     # print(is_sold)
    #     # print(type(is_sold))
    #     # if is_sold=="False":
    #     #     val = True
    #     # print(val)
    #     queryset_list = queryset_list.filter(is_sold = False)
    # else:
    #     is_sold = False
                
    # context={
    #     'listings':queryset_list, 'Min_Price':Min_Price,'Max_Price':Max_Price, 'Area':Area, 'Floors':Floors, 'Bathroom':Bathroom, 
    #     'Bedroom':Bedroom, 'Face':Face, 'City': city, 'Title': Title, 'is_sold': is_sold,

    context={
        'listings':queryset_list, 'Min_Price':Min_Price,'Max_Price':Max_Price, 'Area':Area, 'Floors':Floors, 'Bathroom':Bathroom, 
        'Bedroom':Bedroom, 'Face':Face, 'City': city, 'Title': Title,
    }

    return render(request, "listing_search.html", context)

def LikeView(request, pk):
    listing = get_object_or_404(Listing, id=request.POST.get('listing_id'))
    slug = listing.slug
    liked = False
    if listing.likes.filter(id=request.user.id).exists():
        listing.likes.remove(request.user)
        liked=False
    else:
        listing.likes.add(request.user)
        liked=True
        
    return HttpResponseRedirect(reverse('listing_retrieve', args=[str(slug)]))

class add_comment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self,form):
        form.instance.listing_id=self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('user_specific_listings')


# @login_required
# def listing_create(request):
#     form = ListingForm()
#     if request.method == "POST":
#         form = ListingForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("listings/")

#     context = {
#         "form":form
#     }
#     return render(request, "listing_create.html", context)

# @login_required
# def listing_update(request, pk):
#     listing= Listing.objects.get(id=pk)

#     if request.method == "POST":
#         form = ListingForm(request.POST, instance=listing, files = request.FILES)
#         if form.is_valid():
#             form.save()
#             # context["success"] = True
#             # context["successmsg"] = "Details successfully updated"
#             return HttpResponseRedirect(reverse('listing_retrieve', args=[str(pk)]))
#     else:
#         form = ListingForm(instance=listing)

#     context = {
#         "form":form
#     }
#     return render(request, "listing_update.html", context)

# @login_required
# def listing_retrieve(request,pk):
#     listing= Listing.objects.get(id=pk)
#     # stuff=get_object_or_404(Listing, id=request.kwargs['pk'])
#     # liked=False
#     # if stuff.likes.filter(id=request.user.id).exists():
#     #     liked = True
#     context={
#         "listing":listing
#         # "listing":listing, "liked":liked
#     }
#     return render(request,"listing.html",context)