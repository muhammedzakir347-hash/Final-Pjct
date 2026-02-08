# quraan/management/commands/load_initial_data.py
from django.core.management.base import BaseCommand
from quraan.models import Surah, Reciter, Juz

class Command(BaseCommand):
    help = 'Load initial Quran data'
    
    def handle(self, *args, **options):
        # Create all 114 surahs
        surahs = [
            (1, "Al-Fatihah", "الفاتحة", 7, "Meccan"),
            (2, "Al-Baqarah", "البقرة", 286, "Medinan"),
            (3, "Ali 'Imran", "آل عمران", 200, "Medinan"),
            (4, "An-Nisa", "النساء", 176, "Medinan"),
            (5, "Al-Ma'idah", "المائدة", 120, "Medinan"),
            # ... add all 114
        ]
        
        for number, name, name_ar, ayahs, rev_type in surahs:
            Surah.objects.get_or_create(
                number=number,
                defaults={
                    'name': name,
                    'name_ar': name_ar,
                    'total_ayahs': ayahs,
                    'revelation_type': rev_type
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))