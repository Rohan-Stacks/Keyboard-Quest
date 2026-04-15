from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("levels/", views.level_select, name="levels"),
    path("level/<int:level>/", views.level_page, name="level_page"), #Now using an actual page layout rather than placeholder
]