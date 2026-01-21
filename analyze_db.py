import sqlite3
import json
from django import setup
import os
import sys

# Connect to SQLite directly
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("=== Database Tables ===")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM '{table_name}'")
    count = cursor.fetchone()[0]
    print(f"{table_name}: {count} records")
    
    # Show columns for key tables
    if table_name in ['quraan_surah', 'quraan_reciter', 'quraan_recitation', 'auth_user']:
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        print(f"  Columns: {', '.join(col_names)}")

conn.close()

# Now check with Django
print("\n=== Django Models Count ===")
try:
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alquraan.settings')
    setup()
    
    from quraan.models import Surah, Reciter, Recitation, Juz, Ayah
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    print(f"Users: {User.objects.count()}")
    print(f"Surahs: {Surah.objects.count()}")
    print(f"Reciters: {Reciter.objects.count()}")
    print(f"Recitations: {Recitation.objects.count()}")
    print(f"Juzs: {Juz.objects.count()}")
    print(f"Ayahs: {Ayah.objects.count()}")
    
    # Check if there are audio file fields
    print("\n=== Checking for audio files ===")
    recitations = Recitation.objects.all()[:3]
    if recitations:
        for rec in recitations:
            if hasattr(rec, 'audio_file') and rec.audio_file:
                print(f"Recitation {rec.id} has audio: {rec.audio_file.name}")
            else:
                print(f"Recitation {rec.id}: No audio file field or empty")
except Exception as e:
    print(f"Django check error: {e}")
