from django.conf.urls import url

from . import views
from votes.views import HomeView 

urlpatterns = [
	url(r'^$', HomeView.as_view()),
]
