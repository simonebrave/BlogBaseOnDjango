from django.contrib import admin
from .models import User, Blog, Content
from .forms import RegisterForm

# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Content)
