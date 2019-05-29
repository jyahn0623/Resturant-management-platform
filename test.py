from django.core import serializers
from Main.models import *

serializers.serialize("json", Stock.objects.filter(s_status=False))