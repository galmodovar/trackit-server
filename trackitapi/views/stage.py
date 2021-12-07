"""View module for handling requests about stage types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from trackitapi.models import Stage


class StageView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single stage type

        Returns:
            Response -- JSON serialized stage type
        """
        try:
            stage = Stage.objects.get(pk=pk)
            serializer = StageSerializer(stage, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all stage types

        Returns:
            Response -- JSON serialized list of stage types
        """
        stages = Stage.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StageSerializer(
            stages, many=True, context={'request': request})
        return Response(serializer.data)

class StageSerializer(serializers.ModelSerializer):
    """JSON serializer for stage types
    Arguments:
        serializers
    """
    class Meta:
        model = Stage
        fields = ('id', 'stage')