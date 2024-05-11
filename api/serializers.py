from rest_framework import serializers
from graphics.models import Script
from .models import Numbers, Calls


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


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = "__all__"


class CallSerializer(serializers.ModelSerializer):
    # number = serializers.SerializerMethodField()
    class Meta:
        model = Calls
        fields = "__all__"

    # def get_number(self, obj):
    #     return Numbers.objects.get(pk=obj.pk).number


class CallsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calls
        fields = ['id', 'number']


class CallsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calls
        fields = ['id', 'data', 'status']
