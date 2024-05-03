
from django import forms      
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={
      'placeholder': 'Enter Your password',
      'class': 'form-control'
        
    }))
    
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
      'placeholder': 'please  confirm Your password',
      'class': 'form-control'
        
    }))
    class Meta:
        model = Account
        fields = [ "first_name", "last_name", "phone", "email", "password"]


    def __init__(self, *args, **kwargs ):
        super(RegistrationForm ,self).__init__(  *args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your F name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your L name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Your phone '
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your email'
        
        for fields in self.fields :
            self.fields[fields].widget.attrs['class'] = 'form-control'

    def clean(self):
          cleaned_data = super(RegistrationForm , self).clean()
          password = cleaned_data.get('password')
          confirm_password = cleaned_data.get('confirm_password')
          if password != confirm_password:
            raise forms.ValidationError("password does not matched ")
              
        
         

    
