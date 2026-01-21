import os
import glob

print("=== Checking Local Image Files ===")

# Check for surah images
surah_patterns = [
    "media/surahs/*.png",
    "media/surahs/*.jpg",
    "media/surahs/*.jpeg",
    "static/surahs/*.png",
    "static/surahs/*.jpg",
    "quraan/static/surahs/*.png"
]

print("Looking for surah images...")
surah_images = []
for pattern in surah_patterns:
    for file in glob.glob(pattern):
        surah_images.append(file)

print(f"Found {len(surah_images)} surah image files")

# Check for reciter images  
reciter_patterns = [
    "media/reciters/*.jpg",
    "media/reciters/*.png",
    "media/reciters/*.jpeg",
    "static/reciters/*.jpg"
]

print("\nLooking for reciter images...")
reciter_images = []
for pattern in reciter_patterns:
    for file in glob.glob(pattern):
        reciter_images.append(file)

print(f"Found {len(reciter_images)} reciter image files")

# List files
print("\n=== Sample Files ===")
print("Surah images (first 5):")
for img in surah_images[:5]:
    print(f"  {os.path.basename(img)}")

print("\nReciter images:")
for img in reciter_images:
    print(f"  {os.path.basename(img)}")

# Create a zip file if images exist
if surah_images or reciter_images:
    import zipfile
    zip_name = "quran_images.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for img in surah_images + reciter_images:
            zipf.write(img, os.path.basename(img))
    print(f"\n✓ Created {zip_name} with {len(surah_images) + len(reciter_images)} images")
    print(f"Size: {os.path.getsize(zip_name) / (1024*1024):.2f} MB")
else:
    print("\n❌ No image files found locally!")
    print("Check if images are in: media/surahs/, media/reciters/, or static/ folders")
