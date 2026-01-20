from django.shortcuts import redirect, render, get_object_or_404
from .models import Surah, Reciter, Recitation, Juz,PlayHistory,Favorite,Playlist,PlaylistItem
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import RecitationForm
from django.shortcuts import redirect
import csv
from io import StringIO
from django.db import transaction
from .forms import BulkTextForm




def home(request):
    surahs = Surah.objects.prefetch_related("recitation_set").all()
    reciters = Reciter.objects.all().order_by("name_en")[:8]  # show top 8
    return render(request, "quraan/home.html", {"surahs": surahs,"reciters": reciters,})


def surah_list(request):
    surahs = Surah.objects.prefetch_related("recitation_set").all()
    return render(request, "quraan/surahs.html", {"surahs": surahs})


def reciter_list(request):
    reciters = Reciter.objects.all().order_by("name_en")
    return render(request, "quraan/reciter_list.html", {"reciters": reciters})

def recitation_list(request):
    # browse all recitations (filter optional via query params)
    surah_id = request.GET.get("surah")
    reciter_id = request.GET.get("reciter")
    juz_id = request.GET.get("juz")

    qs = Recitation.objects.select_related("surah", "reciter").all()

    if surah_id:
        qs = qs.filter(surah_id=surah_id)
    if reciter_id:
        qs = qs.filter(reciter_id=reciter_id)
    if juz_id:
        qs = qs.filter(surah__juz__id=juz_id)

    surahs = Surah.objects.all().order_by("number")
    reciters = Reciter.objects.all().order_by("name_en")
    juzs = Juz.objects.all().order_by("number")

    return render(request, "quraan/recitation_list.html", {
        "recitations": qs,
        "surahs": surahs,
        "reciters": reciters,
        "juzs": juzs,
        "selected_surah": surah_id,
        "selected_reciter": reciter_id,
        "selected_juz": juz_id,
    })

def recitation_detail(request, pk):
    recitation = get_object_or_404(
        Recitation.objects.select_related("surah", "reciter"),
        pk=pk
    )
    return render(request, "quraan/recitation_detail.html", {"recitation": recitation})

def surah_detail(request, pk):
    surah = get_object_or_404(Surah, pk=pk)
    recitations = Recitation.objects.filter(surah=surah)
    return render(
        request,
        "quraan/surah_detail.html",
        {
            "surah": surah,
            "recitations": recitations,
        }
    )


@login_required
def recitation_play(request, pk):
    recitation = get_object_or_404(Recitation, pk=pk)

    # history
    PlayHistory.objects.create(user=request.user, recitation=recitation)

    # user playlists
    playlists = Playlist.objects.filter(user=request.user).order_by("-created_at")

    # handle actions
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "favorite":
            Favorite.objects.get_or_create(user=request.user, recitation=recitation)
            return redirect("recitation_play", pk=recitation.pk)

        if action == "add_to_playlist":
            playlist_id = request.POST.get("playlist_id")
            if playlist_id:
                playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
                PlaylistItem.objects.get_or_create(
                    playlist=playlist,
                    recitation=recitation,
                    defaults={"position": playlist.items.count() + 1}
                )
            return redirect("recitation_play", pk=recitation.pk)

    is_favorite = Favorite.objects.filter(user=request.user, recitation=recitation).exists()

    return render(request, "quraan/recitation_play.html", {
        "recitation": recitation,
        "is_favorite": is_favorite,
        "playlists": playlists,
    })


@login_required
def favorites_list(request):
    if request.method == "POST":
        fav_id = request.POST.get("fav_id")
        fav = get_object_or_404(Favorite, id=fav_id, user=request.user)
        fav.delete()
        return redirect("favorites")

    favorites = Favorite.objects.filter(user=request.user).select_related(
        "recitation__surah",
        "recitation__reciter"
    )
    return render(request, "quraan/favorites.html", {"favorites": favorites})

@login_required
def create_playlist(request):
    if request.method == "POST":
        name_en = request.POST.get("name_en")
        name_ar = request.POST.get("name_ar")

        if name_en and name_ar:
            Playlist.objects.create(
                user=request.user,
                name_en=name_en,
                name_ar=name_ar
            )
            return redirect("home")

    return render(request, "quraan/create_playlist.html")

@login_required
def playlists_list(request):
    playlists = Playlist.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "quraan/playlists.html", {"playlists": playlists})

@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(PlaylistItem, id=item_id, playlist=playlist)
        item.delete()
        return redirect("playlist_detail", pk=playlist.pk)

    items = playlist.items.select_related(
        "recitation__surah",
        "recitation__reciter"
    ).order_by("position")

    return render(request, "quraan/playlist_detail.html", {"playlist": playlist, "items": items})


@login_required
def history_list(request):
    history = (
        PlayHistory.objects
        .filter(user=request.user)
        .select_related("recitation__surah", "recitation__reciter")
        .order_by("-played_at")
    )
    return render(request, "quraan/history.html", {"history": history})

def juz_list(request):
    juzs = Juz.objects.all().order_by("number")
    return render(request, "quraan/juz_list.html", {"juzs": juzs})

def juz_detail(request, pk):
    juz = get_object_or_404(Juz, pk=pk)

    surahs = Surah.objects.filter(juz=juz).order_by("number")
    recitations = Recitation.objects.filter(surah__juz=juz).select_related(
        "surah", "reciter"
    )

    return render(request, "quraan/juz_detail.html", {
        "juz": juz,
        "surahs": surahs,
        "recitations": recitations,
    })


def search(request):
    q = request.GET.get("q", "").strip()

    surahs = Surah.objects.none()
    reciters = Reciter.objects.none()
    recitations = Recitation.objects.none()

    if q:
        surahs = Surah.objects.filter(
            Q(name_en__icontains=q) | Q(name_ar__icontains=q)
        ).order_by("number")

        # ✅ Reciters: match by name OR by having recitations in matched surahs
        reciters = Reciter.objects.filter(
            Q(name_en__icontains=q) |
            Q(name_ar__icontains=q) |
            Q(recitation__surah__in=surahs)
        ).distinct().order_by("name_en")

        recitations = Recitation.objects.filter(
            Q(surah__name_en__icontains=q) |
            Q(surah__name_ar__icontains=q) |
            Q(reciter__name_en__icontains=q) |
            Q(reciter__name_ar__icontains=q)
        ).select_related("surah", "reciter")

    return render(request, "quraan/search.html", {
        "q": q,
        "surahs": surahs,
        "reciters": reciters,
        "recitations": recitations,
    })

def reciter_detail(request, pk):
    reciter = get_object_or_404(Reciter, pk=pk)
    recitations = Recitation.objects.filter(reciter=reciter).select_related("surah").order_by("surah__number")
    return render(request, "quraan/reciter_detail.html", {"reciter": reciter, "recitations": recitations})



def toggle_rtl(request):
    current = request.session.get("rtl", False)
    request.session["rtl"] = not current
    return redirect(request.META.get("HTTP_REFERER", "/"))


def toggle_dark(request):
    current = request.session.get("dark", False)
    request.session["dark"] = not current
    return redirect(request.META.get("HTTP_REFERER", "/"))

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after register
            return redirect("home")
    else:
        form = CustomUserCreationForm()


    return render(request, "register.html", {"form": form})



@staff_member_required
def staff_recitation_list(request):
    recitations = Recitation.objects.select_related("surah", "reciter").order_by("surah__number")
    return render(request, "quraan/staff/recitation_list.html", {"recitations": recitations})

@staff_member_required
def staff_recitation_create(request):
    if request.method == "POST":
        form = RecitationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("staff_recitations")
    else:
        form = RecitationForm()
    return render(request, "quraan/staff/recitation_form.html", {"form": form, "mode": "create"})

@staff_member_required
def staff_recitation_update(request, pk):
    rec = get_object_or_404(Recitation, pk=pk)
    if request.method == "POST":
        form = RecitationForm(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            form.save()
            return redirect("staff_recitations")
    else:
        form = RecitationForm(instance=rec)
    return render(request, "quraan/staff/recitation_form.html", {"form": form, "mode": "update"})

@staff_member_required
def staff_recitation_delete(request, pk):
    rec = get_object_or_404(Recitation, pk=pk)
    if request.method == "POST":
        rec.delete()
        return redirect("staff_recitations")
    return render(request, "quraan/staff/recitation_confirm_delete.html", {"rec": rec})


@staff_member_required
def bulk_juz(request):
    form = BulkTextForm(request.POST or None)
    created = 0
    errors = []

    # CSV columns: number,name_en,name_ar
    if request.method == "POST" and form.is_valid():
        f = StringIO(form.cleaned_data["data"])
        reader = csv.reader(f)

        with transaction.atomic():
            for row_num, row in enumerate(reader, start=1):
                if not row or all(not c.strip() for c in row):
                    continue
                try:
                    number = int(row[0].strip())
                    name_en = row[1].strip()
                    name_ar = row[2].strip()
                    obj, was_created = Juz.objects.get_or_create(
                        number=number,
                        defaults={"name_en": name_en, "name_ar": name_ar},
                    )
                    if was_created:
                        created += 1
                except Exception as e:
                    errors.append(f"Line {row_num}: {row} -> {e}")

    return render(request, "quraan/staff/bulk_juz.html", {
        "form": form, "created": created, "errors": errors
    })

@staff_member_required
def bulk_surahs(request):
    form = BulkTextForm(request.POST or None)
    created = 0
    errors = []

    # CSV columns:
    # number,name_en,name_ar,total_ayahs,revelation_type(M/D),juz_numbers(1|2|3)
    if request.method == "POST" and form.is_valid():
        f = StringIO(form.cleaned_data["data"])
        reader = csv.reader(f)

        with transaction.atomic():
            for row_num, row in enumerate(reader, start=1):
                if not row or all(not c.strip() for c in row):
                    continue
                try:
                    number = int(row[0].strip())
                    name_en = row[1].strip()
                    name_ar = row[2].strip()
                    total_ayahs = int(row[3].strip())
                    revelation_type = row[4].strip().upper()  # M or D
                    juz_numbers = row[5].strip() if len(row) > 5 else ""

                    surah, was_created = Surah.objects.get_or_create(
                        number=number,
                        defaults={
                            "name_en": name_en,
                            "name_ar": name_ar,
                            "total_ayahs": total_ayahs,
                            "revelation_type": revelation_type,
                        }
                    )
                    if not was_created:
                        # update basic fields if exists (optional but useful)
                        surah.name_en = name_en
                        surah.name_ar = name_ar
                        surah.total_ayahs = total_ayahs
                        surah.revelation_type = revelation_type
                        surah.save()

                    # assign many-to-many juz
                    if juz_numbers:
                        nums = [int(x.strip()) for x in juz_numbers.split("|") if x.strip()]
                        juz_objs = list(Juz.objects.filter(number__in=nums))
                        surah.juz.set(juz_objs)

                    if was_created:
                        created += 1

                except Exception as e:
                    errors.append(f"Line {row_num}: {row} -> {e}")

    return render(request, "quraan/staff/bulk_surahs.html", {
        "form": form, "created": created, "errors": errors
    })

@staff_member_required
def bulk_reciters(request):
    form = BulkTextForm(request.POST or None)
    created = 0
    errors = []

    # CSV columns: name_en,name_ar,country_en,country_ar
    if request.method == "POST" and form.is_valid():
        f = StringIO(form.cleaned_data["data"])
        reader = csv.reader(f)

        with transaction.atomic():
            for row_num, row in enumerate(reader, start=1):
                if not row or all(not c.strip() for c in row):
                    continue
                try:
                    name_en = row[0].strip()
                    name_ar = row[1].strip()
                    country_en = row[2].strip() if len(row) > 2 else ""
                    country_ar = row[3].strip() if len(row) > 3 else ""

                    obj, was_created = Reciter.objects.get_or_create(
                        name_en=name_en,
                        defaults={
                            "name_ar": name_ar,
                            "country_en": country_en,
                            "country_ar": country_ar,
                        }
                    )
                    if not was_created:
                        obj.name_ar = name_ar
                        obj.country_en = country_en
                        obj.country_ar = country_ar
                        obj.save()

                    if was_created:
                        created += 1

                except Exception as e:
                    errors.append(f"Line {row_num}: {row} -> {e}")

    return render(request, "quraan/staff/bulk_reciters.html", {
        "form": form, "created": created, "errors": errors
    })
@staff_member_required
def bulk_recitations(request):
    form = BulkTextForm(request.POST or None)
    created = 0
    errors = []

    # CSV columns:
    # surah_number,reciter_name_en,recitation_type(murattal/mujawwad),audio_file_path
    #
    # audio_file_path example:
    # recitations/001_al-fatiha_murattal.mp3
    #
    if request.method == "POST" and form.is_valid():
        f = StringIO(form.cleaned_data["data"])
        reader = csv.reader(f)

        with transaction.atomic():
            for row_num, row in enumerate(reader, start=1):
                if not row or all(not c.strip() for c in row):
                    continue
                try:
                    surah_number = int(row[0].strip())
                    reciter_name_en = row[1].strip()
                    recitation_type = row[2].strip()
                    audio_path = row[3].strip()

                    surah = get_object_or_404(Surah, number=surah_number)
                    reciter = get_object_or_404(Reciter, name_en=reciter_name_en)

                    obj, was_created = Recitation.objects.get_or_create(
                        surah=surah,
                        reciter=reciter,
                        recitation_type=recitation_type,
                        defaults={"audio_file": audio_path}
                    )
                    if not was_created:
                        obj.audio_file = audio_path
                        obj.save()

                    if was_created:
                        created += 1

                except Exception as e:
                    errors.append(f"Line {row_num}: {row} -> {e}")

    return render(request, "quraan/staff/bulk_recitations.html", {
        "form": form, "created": created, "errors": errors
    })

@login_required
def add_to_favorites(request):
    if request.method == "POST":
        recitation_id = request.POST.get("recitation_id")
        recitation = get_object_or_404(Recitation, id=recitation_id)
        Favorite.objects.get_or_create(user=request.user, recitation=recitation)
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def add_to_playlist(request):
    if request.method == "POST":
        recitation_id = request.POST.get("recitation_id")
        playlist_id = request.POST.get("playlist_id")
        recitation = get_object_or_404(Recitation, id=recitation_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        playlist.items.create(recitation=recitation, position=playlist.items.count()+1)
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def delete_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    if request.method == "POST":
        playlist.delete()
        return redirect("playlists")
    return render(request, "quraan/confirm_delete_playlist.html", {"playlist": playlist})

