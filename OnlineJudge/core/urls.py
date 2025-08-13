from django.urls import path
from core.views import home_view, submissions_view, problems_view, wip_view

urlpatterns = [
    path('', home_view, name='home'),  # Home Page
    path('wip/', wip_view, name='wip'),  # Work in progress Page
    path('problems/', problems_view, name='problems'),  # Problems Page
    path('submissions/',submissions_view, name='submissions'),  # Submissions Page
]