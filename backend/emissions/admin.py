from django.contrib import admin
from .models import RawEmissionRecord, NormalizedEmissionRecord

admin.site.register(RawEmissionRecord)
admin.site.register(NormalizedEmissionRecord)