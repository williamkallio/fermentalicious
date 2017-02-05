from django.contrib import admin

from .models import Beverage
from .models import Fermentation

admin.site.register(Beverage)
admin.site.register(Fermentation)
