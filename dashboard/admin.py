from django.contrib import admin
from dashboard.models import Measurement, AuthCustodianHashes, Condition, Snapshot, Photos 

admin.site.register(Measurement)
admin.site.register(AuthCustodianHashes)
admin.site.register(Condition)
admin.site.register(Snapshot)
admin.site.register(Photos)


