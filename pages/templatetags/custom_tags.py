from django import template
from accounts.models import CustomUser


register = template.Library()

@register.simple_tag(name='status_create_redirect')
def edit_current_user_status_tag(user):
    return(r"{% url 'status_create' " + CustomUser.objects.get(author=user).pk + ' %}')
