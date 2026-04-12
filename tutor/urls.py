from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("levels/", views.level_select, name="levels"),
    path("level/<int:level>/", views.level_placeholder, name="level_placeholder"),
]