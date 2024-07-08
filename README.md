# Face Recognition Backend

This is the backend component for the Face Recognition System, implemented using FastAPI. This system allows registering students with their face images and corresponding details and recognizing them through captured images. The backend utilizes DeepFace for face recognition and FAISS for efficient similarity search.

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Endpoints](#endpoints)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Face Recognition Backend is responsible for:
- Registering students with their details and face image.
- Recognizing students based on their face image.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **DeepFace**: A lightweight face recognition and facial attribute analysis framework for Python.
- **FAISS**: A library for efficient similarity search and clustering of dense vectors.
- **MongoDB**: A NoSQL database for storing student details and face vectors.
- **PIL**: Python Imaging Library for image processing.

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- MongoDB

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-organization/face-recognition-backend.git
   cd face-recognition-backend
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI Server**

   ```bash
   uvicorn app:app --reload
   ```

   The server should be running at `http://127.0.0.1:8000`.

## Endpoints

### Register a Student

- **URL**: `/register/`
- **Method**: `POST`
- **Parameters**:
  - `file` (form-data): The image file of the student.
  - `name` (form-data): The name of the student.
  - `level` (form-data): The level of the student.
  - `matricule` (form-data): The matricule of the student.
  - `course` (form-data): The course of the student.
  - `department` (form-data): The department of the student.
- **Response**:
  - `200 OK`: Student registered successfully.
  - `400 Bad Request`: No face detected in the image.
  - `415 Unsupported Media Type`: Unsupported media type.

### Recognize a Student

- **URL**: `/recognize/`
- **Method**: `POST`
- **Parameters**:
  - `file` (form-data): The image file to recognize.
- **Response**:
  - `200 OK`: Face recognized with student details.
  - `400 Bad Request`: No face detected in the image.
  - `404 Not Found`: Face not recognized in the database.
  - `415 Unsupported Media Type`: Unsupported media type.

## Usage

1. **Register a Student**

   Use a tool like Postman to send a `POST` request to `/register/` with the required form data and image file.

2. **Recognize a Student**

   Use a tool like Postman to send a `POST` request to `/recognize/` with the image file to be recognized.

## Troubleshooting

- **Backend issues**:
  - Ensure MongoDB is running and accessible.
  - Check if all required Python packages are installed correctly.

- **Common Errors**:
  - `400 Bad Request`: Ensure the image contains a detectable face.
  - `415 Unsupported Media Type`: Ensure the file uploaded is an image.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
```
