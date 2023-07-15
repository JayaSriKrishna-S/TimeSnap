# Template Formats

## Insert Template

- Description: This template is used to insert values into the data source template.
- Accepted Formats: Yaml and Json
## Required Fields:
  - `templateVersion`: The version of the template.
  - `type`: insert
  - `name`: The name of the datasource where the data should be inserted into.
  - `fields`: The list of fields in the template, each with the following sub-fields:
    - `name`: The name of the field in datasource template.
    - `value` : The value with the datatype provided in datasource template
      
## Format:
  - YAML
    
```yaml
- templateVersion: [template_version]
  type: [template_type]
  name: [template_name]
  fields:
    - name: [field_name_1]
      value: [field_value_1]
    - name: [field_name_2]
      value: [field_value_2]
    - name: [field_name_3]
      value: [field_value_3]
    # Add more fields as needed
 ```

  - JSON

    
```json
[
    {
        "templateVersion": "[template_version]",
        "type": "[template_type]",
        "name": "[template_name]",
        "fields": [
            {
                "name": "[field_name_1]",
                "value": "[field_value_1]"
            },
            {
                "name": "[field_name_2]",
                "value": "[field_value_2]"
            }
            // Add more fields as needed
        ]
    }
]
  ```

## HTTP Request Format

`request_service` : insert_template (parameter)\
`file` : select json/yaml file (form-data)


  
