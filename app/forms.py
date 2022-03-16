from django import forms 
from django.forms import ModelForm
from .models import Comment , Post



class StockHistorySearchForm(forms.ModelForm):
    
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
 
	class Meta:
		model = Post
		fields = ['created_date']
  
  
      

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body','active' )
        
        widgets = {
            
            'name': forms.TextInput(attrs = {'class': 'form-control'}),
            'email': forms.TextInput(attrs = {'class': 'form-control'}),
            'body': forms.Textarea(attrs = {'class': 'form-control'}),
            
            
        }



TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class OrderForm(ModelForm):
    class Meta:
        model = Post
        fields = ('__all__' )
        
        widgets = {
            
            
            'promote': forms.Select(choices=TRUE_FALSE_CHOICES,attrs = {'class': 'form-control'}),
            'author': forms.Select(attrs = {'class': 'form-control'}),
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'title2': forms.TextInput(attrs = {'class': 'form-control'}),
            'viewers': forms.TextInput(attrs = {'class': 'form-control'}),
            'text': forms.TextInput(attrs = {'class': 'form-control'}),
            'created_date': forms.SelectDateWidget(attrs = {'class': 'form-control'}),
            'image': forms.FileInput(attrs = {'class': 'form-control'}),
            'details': forms.Textarea(attrs = {'class': 'form-control'}),
            
            
            
            
        }
        
        
    
        



        

            
 