from django.urls import include, path
from rest_framework import routers

from users import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('user/signup/', views.CustomRegisterView.as_view()),
    path('list_profiles/<int:id>/', views.UserProfilesViewSet.as_view()),
    path('show_pdf/<int:pk>/', views.ShowPdf.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]