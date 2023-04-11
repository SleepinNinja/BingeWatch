from django import forms
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError
from django.core import validators
from . import models, views
import django.contrib.auth.hashers
import re

def validate_re(re_func, pattern, string):
    return re_func(pattern, string)

class SearchForm(forms.Form):
    def validate_query(query):
        pattern =  '[a-zA-Z0-9.,''"" ]+'
        result = validate_re(re.match, pattern, query)
        print(result)

        if not result:  
            raise ValidationError(code='invalid', message='Please Enter a valid value ...')
    
    query = forms.CharField(label = '', max_length = 120, strip = True,
        widget = forms.TextInput(
            attrs = {
            'class': 'form-control',
            'placeholder': 'Search for ...',
            }
        ),

        validators = [validate_query]
    )


class SignupForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 100, strip = True, widget = forms.TextInput(attrs = {'class': 'form-control '}))
    first_name = forms.RegexField(label = 'First Name', max_length = 50, strip = True, regex = '[a-zA-Z]{3,}', widget = forms.TextInput(attrs = {'class': 'form-control '}))
    last_name = forms.RegexField(label = 'Last Name', max_length = 50, strip = True, required = False, regex = '[a-zA-Z]{3,}', widget = forms.TextInput(attrs = {'class': 'form-control '}))
    email = forms.EmailField(label = 'Email', widget = forms.TextInput(attrs = {'class': 'form-control '}))
    password = forms.CharField(label = 'Password', max_length = 30, strip = True, widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
    confirm_password = forms.CharField(label = 'Confirm Password', max_length = 30, strip = True, widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
    #profile_image = forms.ImageField(label = "Profile Photo")

    def validate_username(username):
        user_exist = models.CustomUser.objects.get(username = username)

        if user_exist is not None:
            raise ValidationError('Username already exists', code = 'invalid username', params = {'value': '42'})


    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Passwords do not match', code = 'invalid password', params = {'password': 'hello'})


class LoginForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            user = models.CustomUser.objects.get(username = username)

        except models.CustomUser.DoesNotExist:
            raise ValidationError(f'Username { username } does not exist!')

        """
        Will uncomment it when password hashing wil be done

        else:
            if not user.check_password(password):
                raise ValidationError('Entered password is wrong')
        """
    username = forms.CharField(label = 'Username', max_length = 100, strip = True)
    password = forms.CharField(label = 'Password', max_length = 30, strip = True, widget = forms.PasswordInput)


class OTPForm(forms.Form):
    def validate_otp(otp):
        otp_string = str(otp)

        if len(otp_string) != 6:
            raise ValidationError('The length of otp should be 6 digit')

    otp = forms.IntegerField(label = 'OTP', validators = [validate_otp], widget = forms.TextInput)


class ForgotPasswordForm(forms.Form):
    def validate_username(username):
        try:
            user = models.CustomUser.objects.get(username = username)

        except models.CustomUser.DoesNotExist:
            raise ValidationError(f"Username %(username)s does not exist!", params ={'username': username})

    username = forms.CharField(label = 'Username', max_length = 100, validators = [validate_username])


class ChangePasswordForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if len(new_password) < 8:
            raise ValidationError(code = 'short_password', message = 'Password too short')
    
        if new_password != confirm_new_password:
            raise ValidationError(code = 'not_matching', message = 'Password do not match!')

    new_password = forms.CharField(label = 'New Password', max_length = 30, strip = True, widget = forms.PasswordInput)
    confirm_new_password = forms.CharField(label = 'Confirm Password', max_length = 30, strip = True, widget = forms.PasswordInput)


class UpdateUserDetailsForm(forms.Form):
    def to_python(self, data):
        print('inside to python function')
        print('To python data', data)

    def clean(self):
        cleaned_data = super().clean()
        print('cleaning_data')

    def validate_name(name):
        if not name.isalpha():
            raise ValidationError('invalid', 'Enter a valid name')

    username = forms.CharField(label = 'Username', max_length = 100, strip = True)
    first_name = forms.CharField(label = 'First Name', max_length = 30, strip = True, validators = [validate_name])
    last_name = forms.CharField(label = 'Last Name', max_length = 30, strip = True, validators = [validate_name])
    email = forms.EmailField(label = 'Email')
    description = forms.CharField(label = 'Description', widget = forms.Textarea),
    private = forms.BooleanField(label = 'Private Account', widget = forms.CheckboxInput, required = False)


class VideoPlayListForm(forms.ModelForm):
    def validate_name(name):
        if name == None or name == '':
            raise ValidationError('Please enter a name', code = 'required')
        
        pattern = '[a-zA-Z0-9.,''"" ]+'
        result = validate_re(re.fullmatch, pattern, name)

        if not result:
            raise ValidationError('Please enter a valid name', code = 'invalid')
    
    name = forms.CharField(label = 'Playlist name', validators = [validate_name])
    
    class Meta:
        model = models.VideoPlayList 
        fields = ('name', 'genre', 'media_type', 'quality', 'description')


class SingleMediaForm(forms.ModelForm):
    class Meta:
        model = models.SingleMedia
        fields = ('genre', 'media_type', 'quality', 'description')


class MediaForm(forms.ModelForm):
    def validate_name(name):
        pattern = '[a-zA-Z0-9.,''"" ]+'
        result = validate_re(re.fullmatch, pattern, name)
      
        if not result:
            raise ValidationError('%(name)s is not valid name', code = 'invalid', params = {'name': name})
    
    name = forms.CharField(label = 'Episode Name', validators = [validate_name,],
            error_messages = {
                'required': 'Please enter a value',
            }
        )
    
    class Meta:
        model = models.Media
        # need to add cover and file in fields
        fields = ('name',)


class MultiMediaForm(forms.ModelForm):
    def validate_name(name):
        pattern = '[a-zA-Z0-9.,''"" ]+'
        result = validate_re(re.fullmatch, pattern, name)

        if not result:
            raise ValidationError('%(name)s is not a valid name', code='invalid', params={'name': name})
    
    episode_count = forms.IntegerField(
        label='No. of episodes',
        widget=forms.TextInput,
        error_messages={
            'invalid': 'Please enter a valid value',
            'required': 'Please enter a value'
        }
    )

    name = forms.CharField(label='Season name', validators=[validate_name],
            error_messages={
                'required': 'Please enter a value',
            }
        )
  
    class Meta:
        model = models.MultiMedia
        fields = ('name', 'description', 'episode_count')


class BaseMediaFormSet(BaseFormSet):
    def clean(self):
        for form in self.forms:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                name = cleaned_data.get('name')

                if name == None or name == '':
                    raise ValidationError('Enter a value')



class MoreEpisodeForm(forms.Form):
    episode_count = forms.IntegerField(
        label='No. of extra episodes',
        widget=forms.TextInput,
        error_messages={
            'invalid': 'Please Enter a valid value',
            'required': 'Please Enter a value',
        }
    )


class BaseMoreEpisodeFormSet(forms.BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                name = cleaned_data.get('name')

                #if name == None or name == '':
                 #   raise ValidationError('Enter a value', code='invalid')


