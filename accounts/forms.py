from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'age']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].help_text = None


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = ['email']

