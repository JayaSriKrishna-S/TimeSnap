# Template Formats

## Prediction Template

- Description: This template is used to define the prediction configuration for its data source.
- Accepted Formats: Yaml and Json
## Required Fields:
- `templateVersion`: Specifies the version of the template (e.g., "v1").
- `type`: Specifies the type of the template, in this case, "prediction".
- `name`: The name of the prediction template. Must match with its training template.
- `datasource`: The name of the datasource to be used for prediction.

- `selector`: Specifies the fields to select for prediction.
  - `fields`: Lists the fields to be selected.
    - `name`: The name of the field.

- `group`: Specifies the grouping and conditions for prediction.
  - `fields`: Lists the fields to be grouped.
    - `name`: The name of the field.
  - `condition`: Lists the conditions to be applied.
    - `name`: The name of the condition.
    - `field`: The field to apply the condition on.
    - `aggregation`: The type of aggregation to use (e.g., "unique").
    - `match`: The type of match to perform (e.g., "equal").
    - `value`: The value to match against.
    - `action`: The action to be performed based on the condition.

- `sort`: Specifies the sorting for the prediction results.
  - `fields`: Lists the fields to be sorted.
    - `name`: The name of the field.
  - `action`: The sorting action to be performed (e.g., "ascending").

      
## Format:
  - Type 1 - Condition
    
  ```yaml
---
- templateVersion: v1
  type: prediction
  name: [Template Name]
  datasource: [Datasource Name]
  
  selector:
    - fields:
      - name: [Field 1]
      - name: [Field 2]
      - name: [Field 3]
    - action: [Selector Action]
    
  condition:

    - name: [Condition 1]
      field: [Field Name]
      match: [Match Type]
      value: [Condition Value]
      
    - name: [Condition 2]
      field: [Field Name]
      match: [Match Type]
      value: [Condition Value]
      
    - action: [Condition Action]
    
  sort:
    - fields:
      - name: [Field 1]
      - name: [Field 2]
    - action: [Sort Action]

  ```
- Type 2 - Group

```yaml
---
- templateVersion: v1
  type: prediction
  name: [Template Name]
  datasource: [Datasource Name]
  
  selector:
    - fields:
      - name: [Field 1]
    - action: [Selector Action]
  
  group:
    - fields:
      - name: [Field 2]
      
    - condition:
    
      - name: [Condition Name 1]
        field: [Field Name]
        aggregation: [Aggregation Type]
        match: [Match Type]
        value: [Condition Value]
        
      - name: [Condition Name 2]
        field: [Field Name]
        aggregation: [Aggregation Type]
        match: [Match Type]
        value: [Condition Value]
        
      - action: [Condition Action]
  
  sort:
    - fields:
      - name: [Field 3]
    - action: [Sort Action]
  ```

## HTTP Request Format

`request_service` : prediction_template (parameter)\
`file` : select json/yaml file (form-data)





  

  
