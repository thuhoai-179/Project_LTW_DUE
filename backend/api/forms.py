from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        }

        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image','description', 'tags', 'category', 'status']


class Edit_PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','image','description', 'tags', 'category', 'status']
       
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your comment...',
            'rows': 3,
            'class': 'form-control'
        })
    )

    class Meta:
        model = Comment
        fields = ['comment']

    reply_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category title'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }        
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'full_name', 'bio', 'facebook', 'twitter']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ tên'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Về tôi', 'rows': 3}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter URL'}),
        }