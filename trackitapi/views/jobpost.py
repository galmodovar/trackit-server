"""View module for handling requests about Job Posts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackitapi.models import JobPost


class JobPostView(ViewSet):
    """TrackIt job post"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized job post instance
        """
        # Try to save the new job post to the database, then
        # serialize the job post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the job post class
            # and set its properties from what was sent in the
            # body of the request from the client.
            job_post = JobPost.objects.create(
                company=request.data["company"],
                company_url=request.data["companyUrl"],
                role=request.data["role"],
                role_url=request.data["roleUrl"],
                location=request.data["location"],
                industry=request.data["industry"],
            )
            serializer = JobPostSerializer(job_post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single job post

        Returns:
            Response -- JSON serialized job post instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/jobposts/2
            #
            # The `2` at the end of the route becomes `pk`
            job_post = JobPost.objects.get(pk=pk)
            serializer = JobPostSerializer(job_post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single job post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            job = JobPost.objects.get(pk=pk)
            job.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except JobPost.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to job post resource

        Returns:
            Response -- JSON serialized list of job posts
        """
        # Get all game records from the database
        jobs = JobPost.objects.all()


        serializer = JobPostSerializer(
            jobs, many=True, context={'request': request})
        return Response(serializer.data)

class JobPostSerializer(serializers.ModelSerializer):
    """JSON serializer for job posts

    Arguments:
        serializer type
    """
    class Meta:
        model = JobPost
        fields = ('id', 'company', 'company_url', 'role', 'role_url', 'location', 'industry')
        depth = 1