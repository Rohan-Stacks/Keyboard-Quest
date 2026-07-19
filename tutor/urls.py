from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("settings/", views.settings, name="settings"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-vocab/", views.admin_vocab, name="admin_vocab"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("levels/", views.level_select, name="levels"),
    path("level/<int:level>/", views.level_page, name="level_page"), #Now using an actual page layout rather than placeholder
]