from django.contrib import admin
from .models import Juz, Surah, Reciter, Recitation, Favorite, PlayHistory, Playlist, PlaylistItem

# Register your models here.


admin.site.register(Juz)
admin.site.register(Surah)
admin.site.register(Reciter)
admin.site.register(Recitation)
admin.site.register(Favorite)
admin.site.register(PlayHistory)
admin.site.register(Playlist)
admin.site.register(PlaylistItem)
