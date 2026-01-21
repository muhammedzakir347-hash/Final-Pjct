import sqlite3
import os
import shutil
from datetime import datetime

print("Creating clean database export...")

# Create timestamp for backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. First, backup the original
backup_name = f"db_backup_{timestamp}.sqlite3"
shutil.copy2('db.sqlite3', backup_name)
print(f"✓ Created backup: {backup_name}")

# 2. Create a clean version without audio file data
source_conn = sqlite3.connect('db.sqlite3')
dest_conn = sqlite3.connect('clean_db.sqlite3')

# Copy database structure and data
source_conn.backup(dest_conn)

# Clear audio_file column in quraan_recitation table
cursor = dest_conn.cursor()

# Check if audio_file column exists
cursor.execute("PRAGMA table_info('quraan_recitation')")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]

if 'audio_file' in column_names:
    # Set all audio_file values to NULL or empty
    cursor.execute("UPDATE quraan_recitation SET audio_file = NULL")
    print("✓ Cleared all audio file references from recitations")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM quraan_recitation WHERE audio_file IS NOT NULL")
    count = cursor.fetchone()[0]
    print(f"✓ Recitations with audio files remaining: {count}")
else:
    print("⚠ No audio_file column found in quraan_recitation table")

# Also check for image fields that might be large
tables_to_check = ['quraan_reciter', 'quraan_surah']
for table in tables_to_check:
    cursor.execute(f"PRAGMA table_info('{table}')")
    cols = cursor.fetchall()
    for col in cols:
        if 'image' in col[1].lower():
            print(f"✓ Found image column in {table}: {col[1]}")

dest_conn.commit()

# Get sizes
orig_size = os.path.getsize('db.sqlite3') / (1024 * 1024)
clean_size = os.path.getsize('clean_db.sqlite3') / (1024 * 1024)

print(f"\n✓ Original database: {orig_size:.2f} MB")
print(f"✓ Clean database: {clean_size:.2f} MB")
print(f"✓ Size reduction: {orig_size - clean_size:.2f} MB")

# Create SQL dump for inspection
with open('database_dump.sql', 'w', encoding='utf-8') as f:
    for line in dest_conn.iterdump():
        f.write(f'{line}\n')

print(f"✓ Created SQL dump: database_dump.sql")

# Close connections
source_conn.close()
dest_conn.close()

print("\n=== Summary of Data ===")
conn = sqlite3.connect('clean_db.sqlite3')
cursor = conn.cursor()

tables = [
    ('accounts_user', 'Users'),
    ('quraan_surah', 'Surahs'),
    ('quraan_reciter', 'Reciters'),
    ('quraan_recitation', 'Recitations'),
    ('quraan_juz', 'Juzs'),
    ('quraan_playlist', 'Playlists'),
    ('quraan_favorite', 'Favorites'),
    ('django_admin_log', 'Admin Logs')
]

for table, label in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM '{table}'")
        count = cursor.fetchone()[0]
        print(f"{label}: {count}")
    except:
        print(f"{label}: Table not found")

conn.close()

print(f"\n✓ Clean database ready: clean_db.sqlite3")
print("Upload this file to PythonAnywhere!")
