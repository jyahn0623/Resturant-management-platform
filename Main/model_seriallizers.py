from rest_framework import serializers
from Main.models import Menu, Order_sheet

class MenuSerializers(serializers.ModelSerializer):
   class Meta:
       model = Menu
       fields = '__all__'

class OrderCreateSerializers(serializers.Serializer):
    o_table_no = serializers.IntegerField()
    
    def create(self):
        print('hello')


    