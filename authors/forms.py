from collections import defaultdict

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from recipes.models import Recipe

class RegisterForm(forms.ModelForm):
    class Meta:
        #Modelo base
        model = User

        #Campos que estarão no form
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',

        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder':'Type your first name here'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'Type your last name here'
            }),
            'username': forms.TextInput(attrs={
                'placeholder':'Type your username here'
            }),
            'email': forms.TextInput(attrs={
                'placeholder':'Type your email here'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder':'Type your password here'
            }),
        }

    #validar emails diferentes no cadastro
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError(
                'User e-mail is already in use', code ='invalid',
            )

        return email
    
class loginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={
                'placeholder':'Type your  username here'
        }),
    )
    password = forms.CharField(
        widget= forms.PasswordInput(attrs={
            'placeholder':'Type your password here'  
        })
    )

class AuthorRecipeForm(forms.ModelForm):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list) #util para o metodo clean para validacao do formulario

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time', 
                  'preparation_time_unit', 'servings','servings_unit', 
                  'preparation_steps', 'cover'
                ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)
            cleaned_data = self.cleaned_data

            title = cleaned_data.get('title')
            description = cleaned_data.get('description')

            if len(title) < 5:
                self._my_errors['title'].append('Must have at least 5 chars.')

            if title == description:
                self._my_errors['title'].append('Cannot be equal to description')




            if self._my_errors: #mostrar erros na tela
                raise ValidationError(self._my_errors)

            return super_clean

