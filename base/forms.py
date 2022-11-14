from django.forms import ModelForm
from .models import Submission,User
from django.contrib.auth.forms import UserCreationForm


# a model form class that helps create a form with basically all my exisiting fields in a model 
class SubmissionForm(ModelForm):
    class Meta:
        # the model i wamt to create a form for its field
        model=Submission
        # the fields i want to include '__all__' for all 
        # fields='__all__'
        fields=['description']

class CustomUserCreation(UserCreationForm):
    class Meta:
        model=User

        fields= fields = ("username","email","name","password1", "password2")