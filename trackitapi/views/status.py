"""View module for handling requests about status types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from trackitapi.models import Status


class StatusView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single status type

        Returns:
            Response -- JSON serialized status type
        """
        try:
            status = Status.objects.get(pk=pk)
            serializer = StatusSerializer(status, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all status types

        Returns:
            Response -- JSON serialized list of status types
        """
        status = Status.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StatusSerializer(
            status, many=True, context={'request': request})
        return Response(serializer.data)

class StatusSerializer(serializers.ModelSerializer):
    """JSON serializer for status types
    Arguments:
        serializers
    """
    class Meta:
        model = Status
        fields = ('id', 'status')