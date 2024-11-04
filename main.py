from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Model = tf.keras.models.load_model("my_model.keras")
Class_names = ["Early_Blight", "Late_Blight", "Healthy"]


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.get("/ping")
async def ping():
    return "Hello World"


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = Model.predict(img_batch)
    
    predicted_class = Class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {"class ": predicted_class,
            "confidence": float(confidence)}

if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port = "8000")