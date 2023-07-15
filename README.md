# AI Agent: Simplifying Machine Learning for Businesses and Individuals

Welcome to the AI Agent, a cutting-edge tool that revolutionizes the way machine learning is approached by businesses and newcomers. Our AI Agent is here to make your journey into the world of machine learning effortless and hassle-free. No more worrying about complex coding or choosing the right model – the AI Agent takes care of it all.

## Key Features

- **Easy-to-Use Interface**: Say goodbye to writing extensive code. With the AI Agent, you can perform machine learning tasks without any coding knowledge.
- **Seamless Predictions**: Simply provide the input specifications, such as the field you want to predict, and let the AI Agent handle the rest. It automatically generates accurate predictions for you.
- **Newbie-Friendly**: Whether you're a seasoned data scientist or new to the field, the AI Agent is designed to cater to users of all skill levels. No prior machine learning experience required.
- **Versatile Mediator**: The AI Agent acts as a mediator, effortlessly connecting with various online services, allowing you to leverage the power of machine learning across different platforms.


## Index

1. [Supported OS Types](docs/OS-Types.md)
2. [Installation](#installation)
    * [Build from Git](#build-from-git)
    * [Docker](#running-with-docker)
3. [MySQL Workbench Installation](#mysql-workbench-installation)
3. [Initial Configuration](#initial-configuration)
4. [Usage](docs/usage.md)
5. [Sequential Procedure](docs/procedure.md)
6. [Project Components](#project-components)


## Installation

### Build from Git

#### Prerequisites
Before starting the installation process, ensure that you have the following prerequisites:

- Python 3.9 or later installed on your machine.
- Docker installed and properly configured for your operating system.

### Step 1: Set up the Python Environment
Create a new virtual environment (optional but recommended) for your project:
   ```shell
   python3 -m venv myenv
   ```

#### 1. Activate the virtual environment:
On macOS and Linux:
   ```shell
   source myenv/bin/activate
   ```
On Windows:
   ```shell
   myenv\Scripts\activate
   ```

#### 2. Install the project dependencies from the requirements.txt file:
```shell
pip install -r requirements.txt
```

### Step 2: Running the Application Locally
1. Change to the project's root directory
```shell
  cd MODULES
```
2. Execute the following command to start the Uvicorn server locally:
```shell
uvicorn RESTAPI.rest:app --host 0.0.0.0 --port 8000
```
3.The REST API will be accessible at http://localhost:8000. You can interact with it using API testing tools such as curl or Postman.

### Running with Docker

#### Prerequisites
- Before starting the installation process, ensure that you have the following prerequisites:
- Docker installed and properly configured for your operating system.

### Step 1: Building and Running the Docker Container
1. Ensure that Docker is running on your machine.
2. Build the Docker image using the provided Dockerfile. In the terminal or command prompt, navigate to the project's root directory and execute the following command:
```shell
docker build -t my-docker-image .
```
3. Once the image is built, run the Docker container:
```shell
docker run -p 8000:8000 my-docker-image
```
4. The REST API will be accessible at http://localhost:8000, just like when running it locally.

By following these steps, you should be able to set up and run your project either using GitHub or Docker. Choose the appropriate method based on your requirements and preferences.


## MySQL Workbench Installation

To set up the project and use MySQL Workbench, follow the steps below:

### Prerequisites

- Make sure you have MySQL Server installed on your machine. If not, download and install it from the official MySQL website: [MySQL Downloads](https://dev.mysql.com/downloads/)

### Step 1: Download and Install MySQL Workbench

1. Visit the official MySQL website: [MySQL Workbench Downloads](https://dev.mysql.com/downloads/workbench/)

2. Choose the appropriate version of MySQL Workbench for your operating system and click the download link.

3. Once the download is complete, run the installer and follow the installation instructions provided by the setup wizard.

### Step 2: Configure MySQL Connection

1. Launch MySQL Workbench.

2. Click on the **+** button next to "MySQL Connections" to add a new connection.

3. Provide a **Connection Name** for your MySQL connection.

4. Enter the appropriate **Connection Method**, such as Standard TCP/IP over SSH or Standard TCP/IP.

5. Fill in the necessary connection details, including **Hostname**, **Port**, **Username**, and **Password**.

6. Click **Test Connection** to verify that the connection is successful.

7. Once the connection is established, click **OK** to save the MySQL connection.

### Step 3: Create Database Schema

1. In MySQL Workbench, select your established MySQL connection from the "MySQL Connections" pane.

2. Click on the **Schema** tab located in the lower-left section of the window.

3. Right-click anywhere in the **Schema** tab and select **Create Schema**.

4. Provide a name for your new schema and click **Apply**.

5. The new schema will be created and displayed in the **Schema** tab.

### Step 5: Run the Project

1. With MySQL Workbench set up, the MySQL connection established, and the schema created, you are now ready to run your project.

2. Follow the instructions mentioned in the previous sections of this README to install any project dependencies and start the application.

3. Ensure that your project's configuration is set up to connect to the MySQL Server using the appropriate credentials and connection details, including the newly created schema.

By following these steps, you will be able to set up MySQL Workbench, establish a connection to your MySQL Server, create a new schema, and run the application seamlessly.

## MindsDB Cloud Setup

To set up the project and use MindsDB Cloud, follow the steps below:

### Step 1: Sign up for MindsDB Cloud Account

1. Visit the MindsDB website: [MindsDB Cloud](https://www.mindsdb.com/cloud/).

2. Sign up for a MindsDB Cloud account by providing the necessary details and following the registration process.

3. Once registered, you will have access to your MindsDB Cloud account.

### Step 2: Configure MindsDB Integration

1. In your project's codebase, locate the configuration file or module where MindsDB integration is established.

2. Update the configuration with the necessary credentials and connection details provided by your MindsDB Cloud account.

3. Make sure to include any required authentication tokens, API keys, or access credentials in the configuration.

### Step 3: Run the Project

1. With MindsDB Cloud integration configured, you are now ready to run your project.

2. Follow the instructions mentioned in the previous sections of this README to install any project dependencies and start the application.

3. Ensure that your project's code is set up to utilize the MindsDB Cloud integration for machine learning or predictive analytics tasks.

By following these steps, you will be able to set up MindsDB Cloud integration and leverage its capabilities within your project seamlessly.

## Initial Configuration
The application uses environment variables to store the MySQL and MindsDB credentials. You can configure these credentials by updating the .env file in the project directory.

### MySQL Configuration
To configure the MySQL credentials, open the .env file and update the following variables:

```shell
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_mysql_database
```

### MindsDB Configuration
To configure the MindsDB credentials, open the .env file and update the following variables:

```shell
MINDSDB_USERNAME=your_mindsdb_username
MINDSDB_PASSWORD=your_mindsdb_password
```
Replace your_mindsdb_api_key, your_mindsdb_username, and your_mindsdb_password with your actual MindsDB credentials.


## NGROK Setup

#### Step 1: Download Ngrok. Visit https://ngrok.com/download

#### Step 2: Change to the project's root directory
```shell
  cd MODULES
```
#### Step 3: Save the ngrok.exe here



## Project Components

### Source

This project utilizes different technologies for data retrieval, storage, and AI processing. Here are the components involved:

#### HTTP Endpoint

The HTTP endpoint serves as the data source for your project. It allows you to fetch data required for processing from an external API or web service. You can configure the HTTP endpoint by providing the necessary URL, parameters, and authentication credentials, if applicable.

#### MySQL Database

The MySQL database acts as the storage backend for your project. It enables persistent storage and retrieval of data. Your project interacts with the MySQL database to store and retrieve information as needed. You will need to provide the required connection details, such as the host, port, username, and password, to establish a connection with the MySQL database.

#### MindsDB Integration

MindsDB is an integral part of your project's AI capabilities. It is an open-source tool that facilitates the generation of machine learning models using automated machine learning (AutoML). Your project leverages MindsDB to create, train, and deploy machine learning models based on the data obtained from the HTTP endpoint and stored in the MySQL database. To integrate MindsDB into your project, you will need to configure it with your MindsDB username and password.

### Outputs

#### API Output

The API output option allows you to access the predicted values generated by your project through a RESTful API in JSON format. This enables easy integration with other applications or systems. Follow the steps below to configure and utilize the API output:

Set up the API endpoint and define the desired routes for accessing the predicted values.
Implement the necessary API logic to generate the predictions and return them in JSON format.
When the API endpoint is accessed, the predicted values will be returned as a JSON response.
The JSON response will typically include the predicted values for the requested data points or entities. The structure of the JSON response may vary depending on your project's specific requirements and the nature of the predictions.

## License and Copyright
