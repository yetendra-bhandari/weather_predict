from django.contrib import admin

from .models import User, Data

admin.site.register([User, Data])
