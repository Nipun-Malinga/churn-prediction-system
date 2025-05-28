# Bank Customer Churn Prediction System

A full‑stack, production‑ready machine learning system that predicts at‑risk banking customers using XGBoost, Random Forest, and LightGBM. The system includes automated model evaluation and retraining with Apache Airflow, a secure REST API, and an interactive dashboard.

<p align="center">
  <strong>Accuracy: 85% · AUC: 78%</strong><br/>
  XGBoost · LightGBM · Random Forest → Voting Classifier · Apache Airflow · Flask · React + Chakra UI · PostgreSQL · Google Cloud Storage
</p>

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Tech Stack](#tech-stack)
5. [Setup and Installation](#setup-and-installation)
6. [Testing and Evaluation](#testing-and-evaluation)
7. [Future Enhancements](#future-enhancements)

---

## Overview

This project addresses the challenge of predicting bank customer churn using a modular machine learning system. It replaces static rule-based systems with adaptive learning models, using real-world workflows for retraining and evaluation.

Key components include:
- An ensemble voting classifier
- Apache Airflow pipelines for retraining
- A Flask-based REST API
- A React.js + Chakra UI dashboard
- Google Cloud Storage model versioning

---

## Key Features

### 🔢 Data Preprocessing

- Merged features from multiple public sources
- Handled missing values and outliers
- Categorical encoding: One-Hot & Label Encoding
- Balanced dataset using SMOTENC
- Normalized features (Min-Max Scaling)

### Machine Learning Models

- Models: XGBoost, Random Forest, LightGBM
- Ensemble Voting Classifier for improved performance
- Hyperparameter tuning with RandomizedSearchCV
- Calibration Using CalibratedClassifierCV

### Automated Retraining

- Apache Airflow DAGs detect model drift or new untrained data
- Scheduled or manual retraining
- Evaluation using accuracy, precision, recall, F1, and AUC

### Secure Backend API

- Flask server with JWT authentication & bcrypt password hashing
- REST API: predictions, insights, new data, retraining triggers
- PostgreSQL + SQLAlchemy ORM
- Rate limiting with Flask-Limiter

### Frontend Dashboard

- Built with React, Chakra UI, and TypeScript
- View performance metrics, churn risks, confusion matrix
- Manual retraining & model approval controls
- Interactive charts using Recharts

### Cloud & MLOps

- Model versioning via Google Cloud Storage
- Modular architecture following MLOps principles

---

## System Architecture

The system is designed with a modular architecture comprising:

1. **Client-Side:** A React.js and Chakra UI based dashboard for user interaction, data visualization, and system control. It includes user account pages (Login, Edit Account) and data display systems (Dashboard, Model Info Page).
2. **Server-Side:** A Flask-based Python server that hosts the REST API. It includes:
    * An Account System for user management.
    * A Prediction System that uses the deployed ML models.
    * A Database Interface (SQLAlchemy) to interact with the PostgreSQL database.
3. **Airflow Server:** An Apache Airflow instance for orchestrating automated model training and evaluation workflows. This includes a Model Training System and a Model Evaluating System.
4. **Database:** A PostgreSQL database to store user credentials, model metadata, performance metrics, drift information, and customer data for retraining.
5. **Cloud Storage:** Google Cloud Storage for versioning and storing trained machine learning models and preprocessing transformers.

## Tech Stack

* **Backend & Machine Learning:**
    * Python
    * Scikit-Learn (for preprocessing, model building, evaluation)
    * XGBoost
    * LightGBM
    * Pandas, NumPy (for data manipulation)
    * Flask (for REST API server)
    * SQLAlchemy (ORM for PostgreSQL)
    * PyJWT (for JWT authentication)
    * Marshmallow, SciPy
    * Bcrypt (for password hashing)
    * Flask-Limiter (for rate limiting)
* **Frontend:**
    * Vite
    * React.js
    * TypeScript
    * Chakra UI (component library)
    * Recharts (for charts and visualizations)
    * Axios (for API communication)
    * Zustand, Zod, React Hook Form, React Query
* **Workflow Management:**
    * Apache Airflow
* **Database:**
    * PostgreSQL
* **Cloud Services:**
    * Google Cloud Storage (for model storage)
* **Operating System (for development/deployment):**
    * Linux (Ubuntu 22.04 LTS recommended)

## Setup and Installation

**Note:** The system requires a Linux-based operating system to run.

**Minimum System Requirements:**
* OS: Linux (Ubuntu 20.04+ recommended)
* Python 3.9+
* Node.js 18+
* PostgreSQL 12+
* Internet connection for package installation.

### 1. Apache Airflow Installation

* **Step 01:** Add environment variables to the `.bashrc` file:
    ```bash
    export AIRFLOW_HOME="<Airflow_server_location>"
    export AIRFLOW_CONN_CHURN_SERVER_DB="<PostgreSQL_database_connection_string>" # For the app
    export AIRFLOW_DATABASE_SQL_ALCHEMY_CONN="<Airflow_Server_database_connection_string>" # For Airflow metadata
    export GOOGLE_APPLICATION_CREDENTIALS="<Google_Cloud_Storage_service_key_JSON_file_location>"
    ```
* **Step 02:** In the Airflow directory:
    * Create a virtual environment: `python3 -m venv venv`
    * Activate the virtual environment: `source venv/bin/activate`
    * Install Apache Airflow (example version, adjust as needed):
        ```bash
        pip install 'apache-airflow==2.10.5'  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.9.txt"
        ```
        *(Note: The provided document uses `apache-airflow==3.0.0` and `constraints-3.9.txt`. Please verify the correct constraint file for the Airflow version you intend to use.)*
    * Create an Airflow user:
        ```bash
        airflow users create \
            --username admin \
            --firstname Peter \
            --lastname Parker \
            --role Admin \
            --email spiderman@superhero.org \
            --password yoursecurepassword
        ```
    * Install necessary Python libraries for DAGs: `pip install -r requirements.txt` (assuming a requirements file is present in your Airflow DAGs folder).
* **Step 03:**
    * Run the Airflow webserver: `airflow webserver -p 8080`
    * In a new terminal, run the Airflow scheduler: `airflow scheduler`

### 2. Prediction Server (Flask API) Installation

* **Step 01:** Create a `.env` file inside the server directory and add the following:
    ```env
    SECRET_KEY="<Server_Secret_Key>"
    JWT_SECRET_KEY="<Key_for_JWT_authentication>"
    DATABASE_URI="<PostgreSQL_database_URL_for_application>"
    AIRFLOW_URL="<Apache_Airflow_URL>"
    AIRFLOW_USERNAME="<Your_airflow_username>"
    AIRFLOW_PASSWORD="<Your_airflow_password>"
    GOOGLE_APPLICATION_CREDENTIALS="<Path_to_Google_Cloud_service_key_JSON_file>" # If not globally set
    ```
* **Step 02:** In the server directory:
    * Create a virtual environment: `python3 -m venv venv`
    * Activate the virtual environment: `source venv/bin/activate`
    * Install necessary Python libraries: `pip install -r requirements.txt`
    * Run the server: `python3 run.py` (or your main application file)

### 3. System Dashboard (React.js) Installation

* **Step 01:** In the client (frontend) directory:
    * Install necessary libraries: `npm install`
    * Run the UI development server: `npm run dev`

## Testing and Evaluation

The system underwent comprehensive testing:
* **API Testing:** Used Postman for validating endpoints, input validation, JWT authentication, and rate limiting.
* **Model Performance Metrics:** Evaluated models using Accuracy, Precision, Recall, F1-score, and ROC AUC. The ensemble model achieved 85% accuracy and 78% AUC.
* **Drift Detection and Retraining Triggers:** Custom logic successfully detected simulated drift and untrained data, triggering the retraining pipeline.
* **System Security Validation:** Tested against unauthorized access, expired tokens, invalid credentials, and attempts to overload the system.

## Future Enhancements

* **Model Explainability:** Implement SHAP or LIME for better understanding of predictions.
* **Continuous Data Integration:** Add a streaming data pipeline (e.g., Kafka) for real-time data ingestion.
* **CI/CD for ML Models:** Implement automated deployment workflows (e.g., GitHub Actions).
* **Enhanced User Management:** Expand admin panel to support user roles (admin vs. viewer).
* **Email Alerts:** Notify admins about performance drift automatically.
* **Old Model Evaluation System:** Allow admins to evaluate previously deployed models.
* **Dynamic Preprocessing System:** Allow organizations to use their own dataset without modifying the internal code.

---

**Author:** Kodippili T Prabhathiya  
**University:** University of Plymouth / NSBM Green University  
**Project Type:** Final Year Undergraduate Project  
