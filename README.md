# Patient Management API

This project is a FastAPI-based REST API for managing patient health records. It allows users to view all patients, retrieve individual records, and sort patients by metrics such as height, weight, and BMI.

## Features

- View all patient records
- Retrieve a patient by ID
- Sort patients by height, weight, or BMI
- Clean, efficient code structure using FastAPI

## Project Structure

patient_management_api/
│
├── main.py                # FastAPI application code
├── patients_data.json     # Patient data file
├── requirements.txt       # Required Python packages
└── README.md              # Project documentation

## Installation

1. Clone the repository:

   git clone https://github.com/santaji-vhankade/patient_management_api.git
   cd patient_management_api

2. Create and activate a virtual environment:

   python -m venv venv
   venv\Scripts\activate        # For Windows

3. Install dependencies:

   pip install -r requirements.txt

## Running the Application

Run the FastAPI server using Uvicorn:

   uvicorn main:obj --reload

Once running, you can access:

- API Root: http://127.0.0.1:8000/
- Swagger Docs: http://127.0.0.1:8000/docs
- ReDoc Docs: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint               | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | `/`                    | Root message                                 |
| GET    | `/about`               | API description                              |
| GET    | `/view`                | View all patients                            |
| GET    | `/patient/{patient_id}`| View patient details by ID                   |
| GET    | `/sort`                | Sort patients by height, weight, or BMI      |

### Sort Endpoint Example

GET /sort?sort_by=bmi&order=desc

## Example Patient Data (JSON)

{
  "P001": {
    "name": "Ananya Sharma",
    "city": "Guwahati",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 90.0,
    "bmi": 33.06,
    "verdict": "Obese"
  }
}

## Requirements

- Python 3.8 or above
- FastAPI
- Uvicorn

Install them with:

   pip install -r requirements.txt

## Author

Santaji Vhankade  
GitHub: https://github.com/santaji-vhankade

## License

This project is licensed under the MIT License.
