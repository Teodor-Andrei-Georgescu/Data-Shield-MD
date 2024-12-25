# **DataShieldMD**

## **Overview**
This project is a web-based application designed to help users securely process and anonymize datasets using advanced anonymization techniques such as **K-Anonymity**, **L-Diversity**, and **T-Closeness**. Users can upload datasets, apply anonymization algorithms, and manage processed files. The platform ensures data security and user-friendly interactions.

---

## **Features**
- **User Management**:
  - Registration, login, and logout functionality.
  - Authentication to ensure data security.

- **File Management**:
  - Upload `.csv` and `.xlsx` files (with automatic `.xlsx` to `.csv` conversion).
  - Search, filter, and paginate uploaded files.
  - Delete unwanted files.

- **Anonymization Algorithms**:
  - Support for **K-Anonymity**, **L-Diversity**, and **T-Closeness**.
  - Validate and apply algorithms based on user-provided parameters.
  - Save and manage algorithm configurations.

- **Processed Datasets**:
  - Download or delete processed datasets.
  - Search, filter, and paginate processed files.

- **Informational Pages**:
  - Home page with general information.
  - "How We Do It" page explaining the anonymization process.

---

## **Tech Stack**
- **Backend**: Python, Django
- **Frontend**: HTML, and CSS
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **Additional Libraries**: Can be found in requirements.txt file.

---

## **Set up and deployment**

### **Option 1: Docker deployment**
The easiest way to access this application is to run it using docker. I have already created a Docker image for this application and posted it on my Dockerhub.
This image along with instructions can be found at [here](https://hub.docker.com/r/teodorandreigeorgescu/datashieldmd).

### **Option 2: Local Django deployment**

#### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <repository_directory>
```

#### **2. Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **4. Enter DataShieldMD subdirectory**
```bash
#If you do pwd you should be in a directory like this:
#/path/to/your/project/DataShieldMDWebApplication/DataShieldMD/
```

#### **5. Start server**
```bash
python manage.py runserver
```

#### **6. Access the Application**
- Open your browser and navigate to `http://127.0.0.1:8000/`.


---

## **Usage Instructions**

### **1. User Registration and Login**
- Navigate to the **Register** page to create an account.
- Use your credentials to log in.

### **2. Upload a File**
- Navigate to the **Upload Files** page.
- Upload `.csv` or `.xlsx` files. Files are saved securely in your account's directory.
- Use the **search** bar to find files by name or date.

### **3. Apply Anonymization Algorithms**
- Navigate to the **Algorithm Selection** page.
- Select a file and specify the sensitive fields.
- Choose one or more anonymization algorithms and configure their parameters.
  - **K-Anonymity**: Specify a `K` value (minimum 2).
  - **L-Diversity**: Specify `K` and `L` values (both minimum 2).
  - **T-Closeness**: Specify `K` (minimum 2) and `T` (0–1) values.
- Submit the form to anonymize your dataset. The processed file will appear in the **Processed Datasets** page.

### **4. Download or Delete Processed Files**
- Navigate to the **Processed Datasets** page.
- Use the **Download** button to download anonymized files.
- Use the **Delete** button to remove processed files.

---

## **Directory Structure**

```
DATASHIELDMDWEBAPPLICATION/
├── DataShieldMD/           #This is the folder you want to be in to be able to either run docker commpands or django manage.py commands
│   ├── DataShieldMD/       #This is the django project level directory which you dont touch too much.
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py     #In this settings make you make sure to define all project wide settings.
│   │   ├── urls.py         #This urls.py file is where you should indclude urls form apps.
│   │   ├── wsgi.py
├── DataShieldMDApp/        #This is the app level folder which contains all logical for our application.
│   ├── __pycache__/
│   ├── migrations/         #This keep track of all database migrations.
│   ├── static/             #Contains all static file -- CSS, images and videos.
│   ├── templates/          #Contains all HTML templates used in web application.
│   ├── __init__.py
│   ├── admin.py
│   ├── anonypy_utils.py    #Has code to handle all processing of datasets with specified privacy algorithms.
│   ├── apps.py
│   ├── custom_utils.py     #Ignore, this was start of custom implemention of privacy algorithms but never completed.
│   ├── forms.py            #Defines all custom froms used in application.
│   ├── models.py           #Defines all database tables as models and python objects.
│   ├── tests.py
│   ├── urls.py             #Maps urls to their corresponding view functions.
│   ├── views.py            #Defines views and logic behind each page.
├── libs/                   #Modified version of anonypy library.
│   ├── anonypy/
│   ├── ReadMe.md
├── media/                  #Where user uploaded and processed files as stored.
├── .dockerignore
├── db.sqlite3              #Database
├── Dockerfile              #Docker file to build docker image and container.
├── manage.py               #Django utility file to runserver, make migrations, and other django commands.
├── README.Docker.md        #Helper read me for how to use docker commands ro creat docker image and container.
├── requirements.txt        #Contains all installed libraries and versions.
├── venv/                   #My virtual envrionment
└── compose.yaml
```
---

## **Features and Code Overview**

### **1. Models**
- **Dataset**: Tracks uploaded files.
- **AlgorithmParameter**: Stores configurations for algorithms.
- **ProcessedDataset**: Tracks processed files.
- **ActionLog**: Logs user actions for auditing.

### **2. Forms**
- **UserRegistrationForm**: Custom user registration with email validation.
- **FileUploadForm**: Handles file upload validation.
- **AlgorithmSelectionForm**: Manages algorithm selection and parameter validation.

### **3. Views**
- **Authentication**:
  - `register`, `user_login`, `user_logout`.
- **File Management**:
  - `upload_file`: Handles file upload, search, and deletion.
- **Anonymization**:
  - `algorithm_selection`: Applies selected algorithms to files.
- **Processed Files**:
  - `processed_datasets`: Allows downloading or deleting processed datasets.
