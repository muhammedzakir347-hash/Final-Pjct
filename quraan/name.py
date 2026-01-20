import os
import csv

# --- Your folder path ---
folder_path = r"H:\My Drive\my study\final\alquraan\media\recitations\sudais"

# --- Output files ---
txt_file = "file_list.txt"
csv_file = "file_list.csv"

# --- Get all files in folder and subfolders ---
all_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        full_path = os.path.join(root, file)
        all_files.append(full_path)

# --- Save to TXT ---
with open(txt_file, "w", encoding="utf-8") as f:
    for file in all_files:
        f.write(file + "\n")

# --- Save to CSV ---
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["File Path"])  # Header
    for file in all_files:
        writer.writerow([file])

print(f"Total {len(all_files)} files found!")
print(f"Saved to {txt_file} and {csv_file}")
