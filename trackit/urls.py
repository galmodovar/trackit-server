from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from trackitapi.views import register_user, login_user
from trackitapi.views import ApplicationView, JobTypeView, StatusView, StageView, JobPostView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'applications', ApplicationView, 'application')
router.register(r'jobtypes', JobTypeView, 'type')
router.register(r'status', StatusView, 'status')
router.register(r'stages', StageView, 'stage')
router.register(r'jobposts', JobPostView, 'jobpost')




urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
