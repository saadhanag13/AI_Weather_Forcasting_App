import tensorflow as tf

# Load the old model safely
old_model = tf.keras.models.load_model("weather_model_global.h5", compile=False)

# Save it in the new format
old_model.save("weather_model_global_new.keras")

print("✅ Model converted and saved as weather_model_global_new.keras")
