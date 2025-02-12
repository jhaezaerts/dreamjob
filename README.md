# Dream Job App - Docker Learning Project

A simple application designed for learning containerization. This project features a web application where users can submit and view their dream jobs, serving as a practical example of containerizing both frontend and backend services.

## Project Overview

This application consists of:

### Frontend
- Simple HTML/JS interface with a modern, gradient design
- Form to submit dream job entries
- Success notifications and job display functionality

### Backend
- FastAPI server handling job submissions
- Azure Blob Storage for data persistence
- CORS-enabled API endpoints

## Setup Instructions

### Get the source code
1. Create a new folder for the project titled *Container App 'Your name'*
2. Open this folder in VS Code
3. press ctrl+shift+ù and paste ```git clone https://github.com/jhaezaerts/dreamjob.git```

### Create your Azure Container Registry (ACR)

1. Navigate to the Azure Portal and login with your kpmgadvisory account
2. Search for "container registries" in the search bar, and create a new container registry
    - **Resource group:** *Knowledge_Sharing_DSAD*
    - **Registry name:** *AcrDreamjob'Your name'*
    - **Location:** *West Europe*
    - **Pricing plan:** *Basic*
    - **Create**
3. When the container registry is created, go to the resource, navigate to Settings -> Access keys and enable Admin user
4. Navigate to the resource group *Knowledge_Sharing_DSAD* and go to the storage account. In the side blade, navigate to Security + networking -> Access keys. copy the **connection string** and save it for later.

### Build the backend image in cloud shell (it comes with Azure CLI)

1. Start a cloud shell session and enter the following commands:
    - ```mkdir dreamjob<your-name>```
    - ```cd dreamjob<your-name>```
    - ```mkdir backend```
    - ```mkdir frontend```
2. Click 'Manage files' in cloud shell and upload the **only the backend files** from the repository that you cloned
3. In cloud shell, navigate backwards ```cd ..```, ```dir```, until you find the backend files you just uploaded. Move them to the backend folder you created just now in cloud shell.
    
    ```mv app.py Dockerfile requirements.txt dreamjob<your-name>/backend ```

4. From your dreamjob folder, build the backend image and store it in your registry

    ```az acr build --registry <your-registry-name> --image dreamjob-backend-<your-name>:latest backend/```

    ```az acr repository list --name <your-registry-name> --output table```

### Deploy the backend container in Azure Container Instances (ACI)

1. Navigate to the Azure Portal
2. Search for "container instances" and create a new container instance
    - **Resource group:** *Knowledge_Sharing_DSAD*
    - **Name:** *aci-dreamjob-backend-'your name'*
    - **Region:** *West Europe*
    - **Image source:** *Azure Container Registry*
    - **Registry:** *select the registry you created earlier*
    - **Image:** *select the image you just built*
    - **Image tag:** *latest*
    - **DNS name label:** *dreamjob-backend-yourname*
    - **Ports:** *8000*
    - **Ports protocol:** *TCP*
    - **enable container logs:** *NO*
    - **environment variables (key: value)**: 
        - **AZURE_STORAGE_CONNECTION_STRING:** *paste the connection string you copied earlier from the storage account*
            - Mark as secure: Yes
    - **Create**
3. Check if the container is in running state

    ```az container show --resource-group <your-resource-group> --name aci-dreamjob-backend-yourname --output table```

### Build the frontend image in cloud shell

1. In the backend Azure Container Instance, copy the FQDN
2. In the repository you cloned, navigate to the frontend folder and open the script.js file
3. Replace the placeholder BACKEND_URL with the FQDN of the backend container
4. Save the file
5. In cloud shell, click 'Manage files' and upload **only the frontend files** from the repository
6. Navigate backwards ```cd ..``` until you find the frontend files you just uploaded. Move them to the frontend folder in cloud shell

    ```mv script.js Dockerfile index.html dreamjob<your-name>/frontend ```

7. From your dreamjob folder, build the frontend image and store it in your registry

    ```az acr build --registry <your-registry-name> --image dreamjob-frontend-<your-name>:latest frontend/```

    ```az acr repository list --name <your-registry-name> --output table```

### Deploy the frontend container in Azure Container Instances (ACI)

1. Navigate to the Azure Portal
2. Search for "container instances" and create a new container instance
    - **Resource group:** *Knowledge_Sharing_DSAD*
    - **Name:** *aci-dreamjob-frontend-'your name'*
    - **Region:** *West Europe*
    - **Image source:** *Azure Container Registry*
    - **Registry:** *select the registry you created earlier*
    - **Image:** *select the image you just built*
    - **Image tag:** *latest*
    - **DNS name label:** *dreamjob-yourname*
    - **Ports:** *80*
    - **Ports protocol:** *TCP*
    - **enable container logs:** *NO*
    - **Create**
3. Check if the container is in running state

    ```az container show --resource-group <your-resource-group> --name aci-dreamjob-frontend-yourname --output table```

## Submit your dream

1. In the frontend Azure Container Instance, copy the FQDN and visit it in your browser
2. Submit your dream job (check in the developer console if the request is successful)

## Clean up

Delete your resources :)

