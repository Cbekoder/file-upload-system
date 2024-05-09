from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from graphics.models import *
from .models import *


class ScriptTreeView(APIView):
    def get(self, request):
        folder_id = request.query_params.get('pk')
        if folder_id is None:
            return Response({"error": "ID required"}, status=400)
        root_nodes = Script.objects.filter(folder_id=folder_id, parent_id=None)
        serialized_data = ScriptSerializer(root_nodes, many=True).data
        return Response(serialized_data)


class NumberAPIView(APIView):
    def get(self, request):
        numbers=Numbers.objects.all()
        serializer = NumberSerializer(numbers, many=True)
        return Response(serializer.data)

class CallsAPIView(APIView):
    def get(self, request):
        calls=Calls.objects.all()
        serializer = CallSerializer(calls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CallsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            instance_id = request.data['id']
            call_instance = Calls.objects.get(pk=instance_id)
        except KeyError:
            return Response({"error": "Please provide 'id' in the request"}, status=status.HTTP_400_BAD_REQUEST)
        except Calls.DoesNotExist:
            return Response({"error": "Call with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CallsUpdateSerializer(call_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



