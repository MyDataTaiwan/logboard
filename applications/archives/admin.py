from django.contrib import admin
from applications.archives.models import Archive, Records

# Tell admin that the model object has an admin interface
# (show in the admin webpage).
admin.site.register(Records)