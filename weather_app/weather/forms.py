from django import forms


class City(forms.Form):
    """
    Create Form Fields
    """
    city = forms.CharField(widget=forms.TextInput)
    start = forms.DateField(widget=forms.SelectDateWidget())
    end = forms.DateField(widget=forms.SelectDateWidget())
    
