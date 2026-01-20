from django.db import models
from django.conf import settings

class Juz(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name_ar = models.CharField("اسم الجزء", max_length=50)
    name_en = models.CharField("Juz Name", max_length=50)

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

    def __str__(self):
        return self.name_en


class Recitation(models.Model):
    surah = models.ForeignKey(
        Surah,
        on_delete=models.CASCADE,
        verbose_name="السورة"
    )

    reciter = models.ForeignKey(
        Reciter,
        on_delete=models.CASCADE,
        verbose_name="القارئ"
    )

    audio_file = models.FileField(
        upload_to='recitations/',
        verbose_name="ملف التلاوة"
    )

    RECITATION_TYPE = [
        ('murattal', 'Murattal'),
        ('mujawwad', 'Mujawwad'),
    ]
    recitation_type = models.CharField(
        "نوع التلاوة",
        max_length=10,
        choices=RECITATION_TYPE
    )

    def __str__(self):
        return f"{self.surah.name_en} - {self.reciter.name_en}"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    recitation = models.ForeignKey(
        "Recitation",
        on_delete=models.CASCADE,
        verbose_name="التلاوة"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recitation')
        verbose_name = "المفضلة"
        verbose_name_plural = "المفضلة"

    def __str__(self):
        return f"{self.user} - {self.recitation}"


class PlayHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    recitation = models.ForeignKey(
        "Recitation",
        on_delete=models.CASCADE,
        verbose_name="التلاوة"
    )
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']
        verbose_name = "سجل التشغيل"
        verbose_name_plural = "سجل التشغيل"

    def __str__(self):
        return f"{self.user} played {self.recitation}"


class Playlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    name_ar = models.CharField("اسم القائمة", max_length=100)
    name_en = models.CharField("Playlist Name", max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_en


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="القائمة"
    )
    recitation = models.ForeignKey(
        "Recitation",
        on_delete=models.CASCADE,
        verbose_name="التلاوة"
    )
    position = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'recitation')
        ordering = ['position']

    def __str__(self):
        return f"{self.playlist} - {self.recitation}"