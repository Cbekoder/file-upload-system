from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from graphics.models import *


class ScriptTreeView(APIView):
    def get(self, request):
        folder_id = request.query_params.get('pk')
        if folder_id is None:
            return Response({"error": "ID required"}, status=400)
        root_nodes = Script.objects.filter(folder_id=folder_id, parent_id=None)
        serialized_data = ScriptSerializer(root_nodes, many=True).data
        return Response(serialized_data)


