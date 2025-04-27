# backend/model/train_model.py

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt

# ----- Step 1: Load Metadata -----
metadata_path = 'dataset/HAM10000/HAM10000_metadata.csv'
img_dir = 'dataset/HAM10000/images'
metadata = pd.read_csv(metadata_path)

# ----- Step 2: Label Encoding -----
label_list = metadata['dx'].unique().tolist()
label_map = {label: idx for idx, label in enumerate(label_list)}
metadata['label'] = metadata['dx'].map(label_map)

# ----- Step 3: Load and Preprocess Images -----
def load_images(df, img_dir, size=(64, 64)):
    X, y = [], []
    for _, row in df.iterrows():
        img_name = row['image_id'] + '.jpg'
        img_path = os.path.join(img_dir, img_name)
        if os.path.exists(img_path):
            img = load_img(img_path, target_size=size)
            img = img_to_array(img) / 255.0
            X.append(img)
            y.append(row['label'])
    return np.array(X), to_categorical(np.array(y))

print("Loading images (this might take a few minutes)...")
X, y = load_images(metadata, img_dir)

# ----- Step 4: Train-Test Split -----
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----- Step 5: Build CNN Model -----
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=X.shape[1:]),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(label_list), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# ----- Step 6: Train the Model -----
print("Training the model...")
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# ----- Step 7: Save the Model -----
model.save('backend/model/model.h5')
print("Model saved at: backend/model/model.h5")

# ----- Optional: Plot Accuracy -----
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend()
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.show()
