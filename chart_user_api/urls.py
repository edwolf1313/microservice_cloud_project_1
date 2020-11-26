from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url, include
from chart_user_api.views import ChartAccessView
#RefreshAccessView

router = routers.DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path("chart/", ChartAccessView.as_view()),
    path("<int:client_id>/chart/<int:id>/", ChartAccessView.as_view()),
    path("<int:client_id>/chart/", ChartAccessView.as_view()),
    path("<int:chart_id>/chart/delete/", ChartAccessView.as_view()),

    #path("refreshtoken/", RefreshAccessView.as_view())
]
