from django import forms
from .models import Baptism,ParishDetails,LoginDetails,BaptismAdvanced,FieldTable

class BaptismForm(forms.ModelForm):
    class Meta:
        model = Baptism
        fields = [
            'place_of_baptism',
            'date_of_baptism',
            'time_of_baptism',
            'child_name_first',
            'child_name_second',
            'dob',
            'mother_name',
            'father_name',
            'contact_no',
            'email',
        ]
        widgets = {
            'date_of_baptism': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_of_baptism': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



class ParishDetailsForm(forms.ModelForm):
    class Meta:
        model = ParishDetails
        fields = [
            'parent_parish_id', 'name_of_parish', 'place_of_parish', 
            'address', 'email', 'contact_no', 'status'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }



class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=255, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = LoginDetails
        fields = ['user_name', 'password', 'email', 'contact_no', 'parish_id', 'role', 'status']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


class BaptismAdvancedForm(forms.ModelForm):
    class Meta:
        model = BaptismAdvanced
        fields = [
            'basic_baptism_id',
            'q_id',
            'priest_id',
            'question',
            'question_type',
            'compulsary',
            'status',
            'field_id',
            'data_varchar',
        ]
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4}),
        }

class FieldTableForm(forms.ModelForm):
    class Meta:
        model = FieldTable
        fields = ['order_no', 'type', 'data', 'choice', 'q_id', 'status']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.Textarea(attrs={'class': 'form-control'}),
            'choice': forms.Select(attrs={'class': 'form-control'}),
            'order_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'q_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

