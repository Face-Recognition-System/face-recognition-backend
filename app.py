from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from deepface import DeepFace
import numpy as np
import faiss
from pymongo import MongoClient
import base64
from PIL import Image
import io
from bson import ObjectId

app = FastAPI()

# Setup MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['face_db']
collection = db['students']

# Initialize FAISS index
d = 128  # dimension of face vectors, must match the output dimension of DeepFace's model
index = faiss.IndexFlatL2(d)

def get_face_vector(image_data):
    image = Image.open(io.BytesIO(image_data))
    img_array = np.array(image)
    try:
        face_vector = DeepFace.represent(img_array, model_name="Facenet")[0]["embedding"]
    except ValueError as e:
        print(f"Error in face detection: {e}")
        return None
    return np.array(face_vector)

@app.post("/register/")
async def register(file: UploadFile = File(...), name: str = Form(...), level: str = Form(...), matricule: str = Form(...), course: str = Form(...), department: str = Form(...)):
    if file.content_type.startswith('image'):
        image_data = await file.read()
        face_vector = get_face_vector(image_data)
        
        if face_vector is None:
            raise HTTPException(status_code=400, detail="No face detected in the image")

        face_vector_list = face_vector.tolist()

        student = {
            'name': name,
            'level': level,
            'matricule': matricule,
            'course': course,
            'department': department,
            'face_vector': face_vector_list,
            'image': base64.b64encode(image_data).decode('utf-8')
        }

        collection.insert_one(student)
        index.add(np.array([face_vector]))

        return {'result': 'Student registered successfully'}
    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

@app.post("/recognize/")
async def recognize(file: UploadFile = File(...)):
    if file.content_type.startswith('image'):
        image_data = await file.read()
        face_vector = get_face_vector(image_data)
        
        if face_vector is None:
            raise HTTPException(status_code=400, detail="No face detected in the image")

        # Adjust the threshold for face recognition
        D, I = index.search(np.array([face_vector]), 1)
        
        threshold = 1.0  # Adjusted threshold value for better recognition tolerance

        if D[0][0] < threshold:
            student = collection.find_one({'face_vector': face_vector.tolist()})
            if student:
                student['_id'] = str(student['_id'])
                return {'result': 'Face recognized', 'student': student}
            else:
                return JSONResponse(status_code=404, content={'result': 'Face not recognized in database'})
        else:
            return {'result': 'Face not recognized in database'}
    else:
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.43.68", port=8000)