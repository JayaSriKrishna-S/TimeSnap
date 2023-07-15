# Template Formats

## Datasource Template

- Description: This template is used to define the data source configuration.
- Accepted Formats: Yaml and Json
## Required Fields:
  - `templateVersion`: The version of the template.
  - `type`: datasource
  - `name`: The name of the template.
  - `fields`: The list of fields in the template, each with the following sub-fields:
    - `name`: The name of the field.
    - `type`: The data type of the field.
    - `isEmpty` : implies that field may contain null values. (optional) 
      
## Format:
  - YAML
    
  ```yaml
- templateVersion: v1
  type: datasource
  name: [datasource name]
  fields:
    - name: [fieldname]
      type: [SQL datatype]
      isEmpty: [True/False]
    - name: [fieldname]
      type: [SQL datatype]
```
  - JSON

    
  ```json
[
    {
        "templateVersion": "v1",
        "type": "datasource",
        "name": "[datasource name]",
        "fields": [
            {"name": "[fieldname]", "type": "[SQL datatype]", "isEmpty": [True/False]},
            {"name": "[fieldname]", "type": "[SQL datatype]"}
        ]
    }
]
  ```

## HTTP Request Format

`request_service` : datasource_template (parameter)\
`file` : select json/yaml file (form-data)


  
