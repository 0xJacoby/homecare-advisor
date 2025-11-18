# homecare-advisor (ENM156-G17)

## **Setup Instructions**

### 1. Install Python dependencies

Make sure you have Python 3.8+ installed. Then install the required modules from `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note:** Make sure your virtual environment is activated if you are using one.

---

### 2. Run the application

Start the Flask application using:

```bash
python run.py
```

- The database (`journals.db`) will be created automatically in the `./app` folder if it doesn’t exist.
- The server will start on `http://127.0.0.1:5000` by default.

---

### **3. API Endpoints**

#### **Patients**

- `GET /patients/` – List all patients
- `GET /patients/?ssn=<SSN>` – Get a patient by SSN
- `POST /patients/` – Create a new patient
  - Form fields: `ssn`, `firstname`, `surname`

#### **Journal Entries**

**_TO BE DONE_**

---
