from django import forms
from .models import Profiles
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
#     password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', 'name': 'password'}))
#     remember_me = forms.BooleanField(required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'remember_me']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email'] #, 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email2 = forms.EmailField(max_length=150, required=False)
    address = forms.CharField(max_length=255, required=False)
    work_address = forms.Textarea()
    phone = forms.CharField(max_length=32, required=False)
    phone2 = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=150, required=False)
    # certificate = forms.CharField(max_length=15, required=False)# , label='Certificate', widget=forms.TextInput(attrs={'placeholder': 'دكتور, مهندس ...'}))
    # specialist = forms.CharField(max_length=255, required=False)# , label='Specialist', widget=forms.TextInput(attrs={'placeholder': 'الاختصاص العام'}))
    specific_specialist = forms.CharField(max_length=255, required=False) #, widget=forms.TextInput(attrs={'placeholder': 'الاختصاص الدقيق'}))
    publications = forms.Textarea() # widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    bio = forms.Textarea() #widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profiles
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 2}),
            'work_address': forms.Textarea(attrs={'rows': 2}),
  
        }

        
        # widgets = {
        #     'publications': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        # }


# def form_validation_error(form):
#     msg = ""
#     for field in form:
#         for error in field.errors:
#             msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
#     return msg
