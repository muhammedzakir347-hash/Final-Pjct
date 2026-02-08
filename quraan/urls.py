"""
URL configuration for alquraan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from .views import home,toggle_dark, surah_detail,recitation_play,Favorite,favorites_list,reciter_detail,create_playlist,playlists_list,playlist_detail,history_list,juz_list,juz_detail,search,toggle_rtl,register,login_required


urlpatterns = [
    path("", home, name="home"),
    path("surah/<int:pk>/", surah_detail, name="surah_detail"),
    path("reciters/", views.reciter_list, name="reciter_list"),
    path("recitations/", views.recitation_list, name="recitation_list"),
    path("recitations/<int:pk>/", views.recitation_detail, name="recitation_detail"),
    path("recitation/<int:pk>/", recitation_play, name="recitation_play"),
    path("favorites/", favorites_list, name="favorites"),
    path("playlists/create/", create_playlist, name="create_playlist"),
    path("playlists/", playlists_list, name="playlists"),
    path("playlists/<int:pk>/", playlist_detail, name="playlist_detail"),
    path("history/", history_list, name="history"),
    path("juzs/", juz_list, name="juz_list"),
    path("juzs/<int:pk>/", juz_detail, name="juz_detail"),
    path("search/", search, name="search"),
    path("reciters/<int:pk>/", reciter_detail, name="reciter_detail"),
    path("toggle-rtl/", toggle_rtl, name="toggle_rtl"),
    path("toggle-dark/", toggle_dark, name="toggle_dark"),
    path("register/", register, name="register"),
    path("staff/recitations/", views.staff_recitation_list, name="staff_recitations"),
    path("staff/recitations/create/", views.staff_recitation_create, name="staff_recitation_create"),
    path("staff/recitations/<int:pk>/edit/", views.staff_recitation_update, name="staff_recitation_update"),
    path("staff/recitations/<int:pk>/delete/", views.staff_recitation_delete, name="staff_recitation_delete"),
    path("staff/bulk/juz/", views.bulk_juz, name="bulk_juz"),
    path("staff/bulk/surahs/", views.bulk_surahs, name="bulk_surahs"),
    path("staff/bulk/reciters/", views.bulk_reciters, name="bulk_reciters"),
    path("staff/bulk/recitations/", views.bulk_recitations, name="bulk_recitations"),
    path("favorites/add/", login_required(views.add_to_favorites), name="add_to_favorites"),
    path("playlists/add/", login_required(views.add_to_playlist), name="add_to_playlist"),
    path("playlists/<int:pk>/delete/", views.delete_playlist, name="delete_playlist"),
    path("history/log/", views.log_play, name="log_play"),
    path("record-play/", views.record_play, name="record_play"),


    

  

]
