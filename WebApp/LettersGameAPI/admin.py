from django.contrib import admin

# Register your models here.
from .models import Letters, Answers, Words

admin.site.register(Letters)
admin.site.register(Words)
admin.site.register(Answers)
