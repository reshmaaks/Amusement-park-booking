from django import forms
from .models import Account, booking
# from django.contrib.auth.forms 
class BookForm(forms.ModelForm):

    class Meta:
        model=booking
        fields=['date','p1_id','p2_id']


        labels={

            'date':'date',
            'p1_id':'Adult',
            'p2_id':'child',
           
        }
widegts={
    'date':forms.DateInput(attrs={'class':'form-control','placeholder':'Date '}),
    'p1_id':forms.Select(attrs={'class':'form-control'}),
    'p2_id':forms.Select(attrs={'class':'form-control'}),

}  