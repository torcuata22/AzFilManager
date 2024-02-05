# Azure File Manager Django App

This application provides a user-friendly interface to upload, download, and organize files within your Azure Storage. With secure authentication and seamless integration, file management becomes a breeze.

## Features:

- **Azure Storage Integration:** Connect your Django app seamlessly with your Azure Storage account to manage files directly.

- **Full Authentication:** Ensure the security of your files with a robust authentication system, allowing authorized access only.

- **Upload and Download:** Effortlessly upload files to your Azure Storage and download them as needed.

## Getting Started:

### Prerequisites:

Before you start, make sure you have the following:

- ###Azure Storage Account: Set up an Azure Storage account and gather the connection information.

- ###Crete a virtual environment for your porject:

- python -m venv venv

- ###Django 4.2 : Install Django 4.2 on your machine.

### Installation:

1. Clone the repository:

    torcuata22/AzFileManager.git
    

2. Navigate to the project directory:

    cd afm

3. Activate the virtual environment:

    - For Linux/Mac:

        
        source venv/bin/activate
        

    - For Windows:

    
        venv\Scripts\activate
     

4. Install dependencies:

    
    pip install -r requirements.txt
  

6. Set up your environment variables:

    Create a `.env` file with your Azure connection information:

    
MY_SECRET=your-secret
AZURE_STORAGE_ACCOUNT='name of your storage account'
AZURE_STORAGE_ACCOUNT_NAME='storage account name'
AZURE_STORAGE_KEY_NAME='name of your key'
CONTAINER_NAME='the name of your container'
STORAGE_ACCOUNT_KEY='your account key'
CONNECTION_STRING='connection string (from azure)'

    

7. Run migrations:

    python manage.py migrate

8. Start the Django server:

    python manage.py runserver

9. Open your browser and navigate to `http://localhost:8000` to access the Azure File Manager.

## Usage:

1. Log in with your credentials.

2. Upload and download files as needed.

3. Organize and manage your Azure Storage effortlessly.

Enjoy the simplicity of managing your Azure files with the Azure File Manager Django app!

## License:

This project is licensed under the MIT License.

