import os, zipfile

MODEL_PATH = r"C:\Users\saadh\OneDrive\Documents\GitHub\Weather_Forcasting_App\backend\weather_model_global.keras"

print("Exists?", os.path.exists(MODEL_PATH))
print("Files in backend/:", os.listdir(r"C:\Users\saadh\OneDrive\Documents\GitHub\Weather_Forcasting_App\backend"))

# Now use the full path
print("Filesize:", os.path.getsize(MODEL_PATH))


file = "weather_model_global.keras"
print("Exists:", os.path.exists(file))

try:
    with zipfile.ZipFile(file, 'r') as zf:
        print("✅ This is a valid .keras zip file")
        print("Contents:", zf.namelist()[:10])  # first 10 files inside
except zipfile.BadZipFile:
    print("❌ Not a valid .keras file (probably HDF5 or corrupted)")