"""View module for handling requests about job types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from trackitapi.models import JobType, Stage


class JobTypeView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single job type

        Returns:
            Response -- JSON serialized job type
        """
        try:
            job_type = JobType.objects.get(pk=pk)
            serializer = JobTypeSerializer(job_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all job types

        Returns:
            Response -- JSON serialized list of job types
        """
        job_types = JobType.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = JobTypeSerializer(
            job_types, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized JobType instance
        """
        # Try to save the new JobType to the database, then
        # serialize the JobType instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the JobType class
            # and set its properties from what was sent in the
            # body of the request from the client.
            job_type = JobType.objects.create(
                job_type=request.data["jobType"]
          
            )
            serializer = JobTypeSerializer(job_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class JobTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for job types
    Arguments:
        serializers
    """
    class Meta:
        model = JobType
        fields = ('id', 'job_type')
