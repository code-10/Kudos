from django.contrib import admin
from .models import User, Organization, Kudo, KudoConfig

'''
    Registering the models for admin page access
'''

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Kudo)
admin.site.register(KudoConfig)
