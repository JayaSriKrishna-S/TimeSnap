## Usage

### Routes

#### Route: `/`

- Method: GET
- Description: Server Check.
- Response: "Server is up and running."

#### Route: `/show_services`

- Method: GET
- Description: Retrieve the list of available services provided by the server.
- Response: JSON array containing the names of the services.

#### Route: `/show_templates`

- Method: GET
- Description: Retrieve the templates stored in the server based on the specified parameter. Each template has a unique `template_id` associated with it.
- Parameters:
  - `types` (required): The type of templates to retrieve. Use `training` to get all training templates , `prediction` to get all prediction templates and `datasource` to get all datasource templates.
  - template_id (optional) : Use the template Id of the file to view the detailed information of the file. 
- Response: JSON array containing the requested templates.

#### Route: `/choose_service`

- Method: POST
- Description: Select a specific service from the available options.
- Request Body:
  - `request_service` (required): The service to choose from the available options. 
  - `template_id` (required only for training and prediction): The ID of the template.
  - `file` (required only for template creation): The file containing the necessary data for the template request.
- Response: JSON object confirming the selected service.

##### Available request_service and it format
  Template Creation
  - ['datasource_template'](routes/datasource_template.md)
  - ['insert_template'](routes/insert_template.md)
  - ['training_template'](routes/training_template.md)
  - ['prediction_template'](routes/prediction_template.md)

  ML Processing
  - ['training'](routes/training.md)
  - ['prediction'](routes/prediction.md)

#### Route: `/check_status`

- Method: GET
- Description: Check the status of the model training in the cloud. If the training is completed, it returns the accuracy of the model.
- Request Parameters:
  - `template_id` (required): The template ID for which the status is requested.
- Response: JSON object containing the status and accuracy of the model (if available).






