from rest_framework import serializers
from graphics.models import *

class ScriptSerializer(serializers.ModelSerializer):
    child_nodes = serializers.SerializerMethodField()

    class Meta:
        model = Script
        fields = ('question', 'answer', 'child_nodes')

    def get_child_nodes(self, obj):
        children = obj.child_nodes.all()
        if children:
            return ScriptSerializer(children, many=True).data
        return None