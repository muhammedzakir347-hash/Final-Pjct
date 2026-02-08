from django.conf import settings
from django.db import models


class Juz(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f"Juz {self.number}"


class Surah(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name_ar = models.CharField("اسم السورة", max_length=100)
    name_en = models.CharField("Surah Name", max_length=100)
    total_ayahs = models.PositiveSmallIntegerField("عدد الآيات")

    REVELATION_TYPE = [
        ("M", "Makki"),
        ("D", "Madani"),
    ]
    revelation_type = models.CharField(
        "نوع النزول",
        max_length=1,
        choices=REVELATION_TYPE
    )

    juz = models.ManyToManyField(
        Juz,
        verbose_name="الجزء",
        blank=True
    )

    image = models.ImageField(
        upload_to="surahs/",
        blank=True,
        null=True,
        verbose_name="صورة السورة"
    )

    @property
    def image_url(self) -> str:
        # Works for S3 and local automatically
        return self.image.url if self.image else ""

    def __str__(self):
        return f"{self.number} - {self.name_en}"


class Reciter(models.Model):
    name_ar = models.CharField("اسم القارئ", max_length=100)
    name_en = models.CharField("Reciter Name", max_length=100)

    country_ar = models.CharField("الدولة", max_length=100, blank=True)
    country_en = models.CharField("Country", max_length=100, blank=True)

    image = models.ImageField(
        upload_to="reciters/",
        blank=True,
        null=True,
        verbose_name="صورة القارئ"
    )

    @property
    def image_url(self) -> str:
        return self.image.url if self.image else ""

    def __str__(self):
        return self.name_en


class Recitation(models.Model):
    RECITATION_TYPES = [
        ("murattal", "Murattal"),
        ("mujawwad", "Mujawwad"),
        ("tajweed", "Tajweed"),
        ("other", "Other"),
    ]

    reciter = models.ForeignKey(
        Reciter,
        on_delete=models.CASCADE,
        related_name="recitations"
    )
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        related_name="recitations"
    )

    audio_file = models.FileField(
        upload_to="recitations/",
        blank=True,
        null=True,
        verbose_name="Audio File"
    )

    recitation_type = models.CharField(
        max_length=50,
        blank=True,
        default="murattal",
        choices=RECITATION_TYPES
    )

    @property
    def audio_url(self) -> str:
        return self.audio_file.url if self.audio_file else ""

    def __str__(self):
        return f"{self.reciter.name_en} - {self.surah.name_en} ({self.recitation_type})"

class Playlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlists"
    )
    name = models.CharField(max_length=200, default="My Playlist")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user}"



class PlaylistItem(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name="items"
    )
    recitation = models.ForeignKey(
        Recitation,
        on_delete=models.CASCADE,
        related_name="playlist_items"
    )
    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("playlist", "recitation")]



class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    recitation = models.ForeignKey(
        Recitation,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "recitation")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.recitation}"


class PlayHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="play_history"
    )
    recitation = models.ForeignKey(
        Recitation,
        on_delete=models.CASCADE,
        related_name="play_history_entries"
    )
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-played_at"]

    def __str__(self):
        return f"{self.user} played {self.recitation} at {self.played_at}"
