from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Listing, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["Title", 
        "Location", 
        "City", 
        "Price", 
        "Bedroom", 
        "Bathroom", 
        "Floors", 
        "Parking", 
        "Face", 
        "Area", 
        "Road_Width",
        "Road_Type", 
        "Build_Area", 
        "Amenities", 
        "Contact_number", 
        "Contact_mail",
        "Image",
        "is_sold",
        "Description"
        ]
        labels = {
            "is_sold": "Sell Status (Please tick if your real estate has already been sold.)",
            "Price": "Price (in NPR)",
            "Area": "Area (in square feet)",
            "Build_Area": "Build Area (in square feet)",
            "Road_Width": "Road Width (in feet)",
            "Bedroom": "Number of Bedrooms",
            "Bathroom": "Number of Bathrooms",
            "Floors": "Number of Floors",
            "Parking": "Number of Parking",
        }
        widgets = {
            'Title':forms.TextInput(attrs={'class':'form-control'}),
            'Location':forms.TextInput(attrs={'class':'form-control'}),
            'City':forms.TextInput(attrs={'class':'form-control'}), 
            'Price':forms.NumberInput(attrs={'class':'form-control'}), 
            'Bedroom':forms.NumberInput(attrs={'class':'form-control'}),
            'Bathroom':forms.NumberInput(attrs={'class':'form-control'}),
            'Floors':forms.NumberInput(attrs={'class':'form-control'}),
            'Parking':forms.NumberInput(attrs={'class':'form-control'}),
            'Face':forms.TextInput(attrs={'class':'form-control'}),
            'Area':forms.NumberInput(attrs={'class':'form-control'}),
            'Road_Width':forms.NumberInput(attrs={'class':'form-control'}),
            'Road_Type':forms.TextInput(attrs={'class':'form-control'}),
            'Build_Area':forms.NumberInput(attrs={'class':'form-control'}),
            'Amenities':forms.TextInput(attrs={'class':'form-control'}),
            'Description':forms.Textarea(attrs={'class':'form-control'}),
            'Contact_number':forms.NumberInput(attrs={'class':'form-control'}),
            'Contact_mail':forms.EmailInput(attrs={'class':'form-control'}),
            'Image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'is_sold':forms.CheckboxInput(attrs={'class':'w-8 h-8'}),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", 
        "body"
        ]
        labels = {
            'name':'Name',
            'body':'Comment'
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label='')
    # first_name = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter name'}))
    first_name = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            # self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'