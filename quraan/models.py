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
        ('M', 'Makki'),
        ('D', 'Madani'),
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
        upload_to='surahs/',
        blank=True,
        null=True,
        verbose_name="صورة السورة"
    )
    
    def get_image_url(self):
        """Return the image URL."""
        if not self.image:
            return ""
        image_value = str(self.image)
        if image_value.startswith(('http://', 'https://')):
            return image_value
        return f"/media/{image_value}"
    
    def __str__(self):
        return f"{self.number} - {self.name_en}"


class Reciter(models.Model):
    name_ar = models.CharField("اسم القارئ", max_length=100)
    name_en = models.CharField("Reciter Name", max_length=100)
    
    country_ar = models.CharField("الدولة", max_length=100, blank=True)
    country_en = models.CharField("Country", max_length=100, blank=True)
    
    image = models.ImageField(
        upload_to='reciters/',
        blank=True,
        null=True,
        verbose_name="صورة القارئ"
    )
    
    def get_image_url(self):
        """Return the image URL."""
        if not self.image:
            return ""
        image_value = str(self.image)
        if image_value.startswith(('http://', 'https://')):
            return image_value
        return f"/media/{image_value}"
    
    def __str__(self):
        return self.name_en


class Recitation(models.Model):
    reciter = models.ForeignKey(Reciter, on_delete=models.CASCADE, related_name='recitations')
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE, related_name='recitations')
    audio_file = models.FileField(upload_to='recitations/', blank=True, null=True)
    recitation_type = models.CharField(max_length=50, blank=True)
    audio_file = models.FileField(
        upload_to='recitations/',  # This will create 'recitations/' folder in S3
        blank=True,
        null=True,
        verbose_name="Audio File"
    )
    def __str__(self):
        return f"{self.reciter.name_en} - {self.surah.name_en}"
    
    def get_audio_url(self):
        """Return the audio URL."""
        if not self.audio_file:
            return ""
        audio_value = str(self.audio_file)
        if audio_value.startswith(('http://', 'https://')):
            return audio_value
        return f"/media/{audio_value}"


class Playlist(models.Model):
    name = models.CharField(max_length=200, default="My Playlist")  # Add default here
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    recitation = models.ForeignKey(Recitation, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.playlist.name} - {self.recitation}"


class Favorite(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='favorites')
    recitation = models.ForeignKey(Recitation, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'recitation']
    
    def __str__(self):
        return f"{self.user.username} - {self.recitation}"


class PlayHistory(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='play_history')
    recitation = models.ForeignKey(Recitation, on_delete=models.CASCADE, related_name='play_history')
    played_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} played {self.recitation} at {self.played_at}"
