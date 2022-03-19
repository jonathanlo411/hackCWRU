from django import forms

class UserCreation(forms.Form):
    username = forms.CharField(label=False, min_length=3, max_length=20, widget=forms.TextInput(attrs={'class':'su-field', 'placeholder':'Username'}))
    password = forms.CharField(label=False, min_length=6, max_length=20, widget=forms.TextInput(attrs={'class':'su-field', 'placeholder':'Password (6 Characters Minimum)', 'type':'password'}))