"""View module for handling requests about applications"""
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from trackitapi.models import Application, JobType, Applicant, Stage, Status, JobPost, applicant, application


class ApplicationView(ViewSet):
    """Level up application"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized application instance
        """

        # Uses the token passed in the `Authorization` header
        applicant = Applicant.objects.get(user=request.auth.user)

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `propertyId` in the body of the request.
        stage = Stage.objects.get(pk=request.data["stageId"])
        new_status = Status.objects.get(pk=request.data["statusId"])
        job_post = JobPost.objects.get(pk=request.data["jobId"])

        # Try to save the new application to the database, then
        # serialize the application instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Application class
            # and set its properties from what was sent in the
            # body of the request from the client.
            application = Application.objects.create(
                notes=request.data["notes"],
                response=request.data["response"],
                date_applied=request.data["date_applied"],
                stage=stage,
                applicant=applicant,
                status=new_status,
                job_post=job_post
            )
            application.skills.set(request.data['skills'])
            serializer = ApplicationSerializer(application, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single application

        Returns:
            Response -- JSON serialized application instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/applications/2
            #
            # The `2` at the end of the route becomes `pk`
            application = Application.objects.get(pk=pk)
            serializer = ApplicationSerializer(application, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an application

        Returns:
            Response -- Empty body with 204 status code
        """
        applicant = Applicant.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        application = Application.objects.get(pk=pk)
        application.notes = request.data["notes"]
        application.response = request.data["response"]
        application.date_applied = request.data["date_applied"]
        application.skills.set(request.data['skills'])
        application.applicant = applicant
        

        stage = Stage.objects.get(pk=request.data["stageId"])
        application.stage =stage
        stage.save()
        
        new_status = Status.objects.get(pk=request.data["statusId"])
        application.status =new_status
        new_status.save()
        
        job_post = JobPost.objects.get(pk=request.data["jobId"])
        application.job_post = job_post
        job_post.save()
        
        application.save()
        

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single application

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            application = Application.objects.get(pk=pk)
            application.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Application.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to application resource

        Returns:
            Response -- JSON serialized list of applications
        """
        # Get all game records from the database
        applicant = Applicant.objects.get(user=request.auth.user)
        applications = Application.objects.filter(applicant=applicant)
        search = self.request.query_params.get('q', None)
        if search is not None:
            applications = applications.filter(
                Q(skills__job_type__icontains=search) |
                Q(job_post__company__icontains=search) |
                Q(stage__stage__icontains=search) |
                Q(notes__icontains=search) |
                Q(status__status__icontains=search)
            )
        

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all Frontend Jobs
        job_type = self.request.query_params.get('type', None)
        if job_type is not None:
            applications = applications.filter(job_type__id=job_type)

        serializer = ApplicationSerializer(
            applications, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class JobTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for job types
    Arguments:
        serializers
    """
    class Meta:
        model = JobType
        fields = ('id', 'job_type')

class ApplicationSerializer(serializers.ModelSerializer):
    """JSON serializer for application

    Arguments:
        serializer type
    """
    skills = JobTypeSerializer(many=True)
    class Meta:
        model = Application
        fields = ('id', 'notes', 'response', 'date_applied', 'applicant', 'job_post', 'stage', 'status', 'skills')
        depth = 1
