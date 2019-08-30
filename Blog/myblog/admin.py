from django.contrib import admin
from .models import User, Blog, Comment
from .forms import RegisterForm

# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)
