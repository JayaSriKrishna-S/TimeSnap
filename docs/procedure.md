## Procedure: Setting up and Using the AI Agent

1. **Install Dependencies:**
   - Follow the installation instructions mentioned in the "Installation" section of the README file to install all the required dependencies for the project.

2. **Create MindsDB and MySQL Workbench Accounts:**
   - Sign up for a MindsDB account by visiting their website and creating a new account.
   - Sign up for a MySQL Workbench account by visiting their website and creating a new account.

3. **Create a Schema in MySQL Workbench:**
   - Open MySQL Workbench and connect to your MySQL database using the provided credentials.
   - Create a new schema in the database where you will store the project's data. Name the schema according to your preference.

4. **Update Credentials in .env File:**
   - In the root folder of the project, locate the `.env` file.
   - Open the `.env` file in a text editor and update the credentials with the appropriate values for the MindsDB and MySQL Workbench accounts.

5. **Create a Datasource Template:**
   - Use the provided HTTP endpoint to create a datasource template. This template defines the structure and data types of the input data.
   - Configure the datasource template by specifying the required fields and their corresponding data types.
   - Upload the datasource template to the AI Agent.

6. **Push Values into the Datasource Template:**
   - Use the insert template functionality to push values into the previously created datasource template.
   - Provide the necessary field values for each entry to populate the datasource template with data.

7. **Create Training and Prediction Templates:**
   - Create a training template to define the machine learning model's training process.
   - Create a prediction template to define how the model should make predictions based on input data.

8. **Start Training on the Training Template:**
   - Initiate the training process by executing the training template.
   - The AI Agent will use the data in the datasource template to train the machine learning model.
   - Monitor the training progress and wait until it completes.

9. **Predict Values using the Prediction Template:**
   - Once the training is complete, you can use the prediction template to make predictions.
   - Provide the necessary input data to the prediction template, and the AI Agent will generate predictions based on the trained model.
   - Retrieve and utilize the predicted values for further analysis or decision-making.
