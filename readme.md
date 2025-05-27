# Bank Customer Churn Prediction System Using Machine Learning

**Module:** PUSL3190 Computing Individual Project
**Programme:** BSc (Hons) Software Engineering
**Student:** Kodippili T Prabhathiya (10899663)
**Supervisor:** Mr. Gayan Perera

## Overview

This project presents a full-stack, automated bank customer churn prediction system. It integrates supervised machine learning models (XGBoost, Random Forest, LightGBM) with an ensemble voting classifier for robust predictions. The system aims to address the significant challenge of customer churn in the banking sector, which impacts profitability and customer relationships. Traditional rule-based systems often lack the adaptability to evolving customer behavior, a gap this project seeks to fill by leveraging machine learning and MLOps practices.

The system features an autonomous pipeline based on Apache Airflow for model evaluation and retraining, triggered by performance drift. It includes a cloud-based model versioning system with a secure REST API server built with Flask. A React.js-based dashboard provides real-time model insights and configuration options. The ensemble model achieved 85% accuracy and an AUC of 78% after handling class imbalance using SMOTENC. This solution offers a scalable and maintainable approach for banks to proactively retain high-risk customers, thereby reducing churn-related losses and enhancing operational decision-making.

## Key Features

* **Comprehensive Data Preprocessing:**
    * Engineered a custom dataset by integrating features from multiple public sources.
    * Handled missing values, detected and capped outliers.
    * Performed categorical encoding (One-Hot and Label Encoding).
    * Addressed class imbalance using SMOTENC.
    * Normalized features using Min-Max Scaling.
    * Ensured feature consistency, for example, between `has_credit_card` and `card_type`.
* **Advanced Machine Learning Modeling:**
    * Utilized supervised machine learning algorithms: XGBoost, Random Forest, and LightGBM.
    * Implemented an Ensemble Voting Classifier combining individual model predictions for improved reliability and performance.
    * Optimized hyperparameters using Randomized SearchCV.
* **Automated Retraining and Evaluation:**
    * Apache Airflow-based autonomous pipeline for scheduled model evaluation and retraining.
    * Automated retraining triggered by performance drift detection or new untrained data.
    * Model performance monitoring using metrics like accuracy, precision, recall, and F1-score.
* **Robust Backend System:**
    * RESTful API server built with Flask providing endpoints for predictions, model analytics, dataset insights, new data ingestion, and manual retraining triggers.
    * Secure API with JWT (JSON Web Tokens) authentication and rate limiting.
    * User password encryption using bcrypt.
    * PostgreSQL database for storing model information, insights, churn data, and user data.
    * SQLAlchemy as ORM for database interactions.
* **Interactive Frontend Dashboard:**
    * User-friendly interface developed with React.js, TypeScript, and Chakra UI.
    * Real-time visualization of churn risk scores, model performance indicators (accuracy, precision, recall, confusion matrix, F1 score), performance history, and dataset insights using Recharts.
    * Controls for manual retraining, new trained model approval, and Airflow DAG insights.
* **Cloud Integration & MLOps:**
    * Cloud-based model versioning and storage using Google Cloud Storage.
    * Adherence to MLOps practices for a scalable and maintainable solution.

## System Architecture

The system is designed with a modular architecture comprising:
1.  **Client-Side:** A React.js and Chakra UI based dashboard for user interaction, data visualization, and system control. It includes user account pages (Login, Edit Account) and data display systems (Dashboard, Model Info Page).
2.  **Server-Side:** A Flask-based Python server that hosts the REST API. It includes:
    * An Account System for user management.
    * A Prediction System that uses the deployed ML models.
    * A Database Interface (SQLAlchemy) to interact with the PostgreSQL database.
3.  **Airflow Server:** An Apache Airflow instance for orchestrating automated model training and evaluation workflows. This includes a Model Training System and a Model Evaluating System.
4.  **Database:** A PostgreSQL database to store user credentials, model metadata, performance metrics, drift information, and customer data for retraining.
5.  **Cloud Storage:** Google Cloud Storage for versioning and storing trained machine learning models and preprocessing transformers.

*(Refer to Figure 1 in the report for the High-Level System Architecture Diagram and Figure 2 for the Database ER Diagram)*

## Technologies Used

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
* Python 3.12+
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
        pip install 'apache-airflow==3.0.0' --constraint "[https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.9.txt](https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.9.txt)"
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
        *(Note: The document command for user creation does not include password, it might prompt or require setting via UI/other means)*
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
* **Unit and Integration Testing:** Verified individual functions (data preprocessing, model evaluation) and interactions between components (dashboard to API, API to model).
* **API Testing:** Used Postman and Pytest for validating endpoints, input validation, JWT authentication, and rate limiting.
* **Model Performance Metrics:** Evaluated models using Accuracy, Precision, Recall, F1-score, and ROC AUC. The ensemble model achieved 85% accuracy and 78% AUC after SMOTENC.
* **Drift Detection and Retraining Triggers:** Custom logic successfully detected simulated drift and untrained data, triggering the retraining pipeline.
* **System Security Validation:** Tested against unauthorized access, expired tokens, invalid credentials, and attempts to overload the system.

## Future Enhancements

* **Model Explainability:** Implement SHAP or LIME for better understanding of predictions.
* **Continuous Data Integration:** Add a streaming data pipeline (e.g., Kafka) for real-time data ingestion.
* **CI/CD for ML Models:** Implement automated deployment workflows (e.g., GitHub Actions).
* **Enhanced User Management:** Expand admin panel to support user roles (admin vs. viewer).
* **Email Alerts:** Notify admins about performance drift automatically.
* **Old Model Evaluation System:** Allow admins to evaluate previously deployed models.
* **Dynamic Preprocessing System:** Allow organizations to use there own dataset without modifying the internal code.

---

*This README is generated based on the "Bank Customer Churn Prediction System Using Machine Learning - Final Report" by Kodippili T Prabhathiya.*