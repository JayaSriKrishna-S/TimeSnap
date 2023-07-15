import json
import os
import glob
import re


def parser(data,req):
  if(req=='datasource_template'):
    req_fields_datasource={"templateVersion":str,"type":str,"name":str,"fields":list}
    datasource_optional={}
    inside_fields ={'name':str,"type":str,'isEmpty':bool}
    inside_fields_optional={"isEmpty":True}
    a= check_for_fields(data,req_fields_datasource,inside_fields,datasource_optional,inside_fields_optional)
    if(a!=1):
       return str(a)
    c=check_details(data)
    working_folder = os.getcwd()
    filename = os.path.join(working_folder,"RESTAPI", "DATASOURCE_TEMPLATES",str(c)+".json")
    try: 
     with open(filename, 'x') as file:
        json.dump(data, file)
     return "1"
    except Exception  as e:
      return str(e)
       
  if(req=='insert_template'):
      req_fields_datasource={"templateVersion":str,"type":str,"name":str,"fields":list}
      datasource_optional={}
      inside_fields ={'name':str,"value":"dontCare"} ##integer check
      inside_fields_optional={}
      a=check_for_fields(data,req_fields_datasource,inside_fields,datasource_optional,inside_fields_optional)
      if a!=1:
        b=check_for_fields2(data)
        if b==1:
           return "1"
        else:
           return b
           
      template_name=check_details(data)
      if(not check_template_exits(template_name,"DATASOURCE_TEMPLATES")):
        return "Template not found"
      a=match_template_fields(template_name,data)
      if(a!=1):
       return a
      return "1"
     
  if(req=='training_template' or req=='prediction_template'):
    
    if(req=='training_template'):
       mode=0
    else:
       mode=1   
    res=check_predict(data,mode)
    if(type(res)==tuple):
       valid,save_type,save_name=res
    else:
       return res   
    if(valid!=True):
       return valid
    location=""
    if save_type.lower() == "training":
       location="TRAINING_TEMPLATES"
    elif save_type.lower()=="prediction":
       location="PREDICTION_TEMPLATES" 
    else:
       return "Wrong type expected training or prediction"

    if(check_template_exits(save_name,location)):
       return "Template exist"
    
    working_folder = os.getcwd()
    filename = os.path.join(working_folder,"RESTAPI", location,save_name+".json")
  
    try: 
     with open(filename, 'x') as file:
        json.dump(data, file)
     return "1"
    except Exception  as e:
      return str(e)
   
  
    
################### MAIN CHECK FOR COLUMNS 

def check_for_fields(data,req_fields_datasource,inside_fields,datasource_optional,io):
   
   for i in data:
     for item,val in i.items():
        if(item in req_fields_datasource.keys()):
           if(item=='name'):
              data[0]['name']=data[0]['name'].lower()
           if(type(val)==req_fields_datasource[item]):
             if(type(val)==list):
               a=check_inside_list(val,inside_fields,io)
               if(a=="V"):
                 req_fields_datasource.pop(item)
                 continue
               else:
                 return a
             else:  
              req_fields_datasource.pop(item)
              continue
           else:
            return "Format Error. \'"+str(item)+"\' has wrong type format"
        else:
          return "Key Error. \'"+str(item)+"\' doesn't belong to the template"


   do=list(req_fields_datasource.keys())
   dop=list(datasource_optional.keys())
   check =  all(item in dop for item in do)
          
   if( not bool(req_fields_datasource) or check):   
     return 1    
   return "Value Missing Error. All the field of template are not provided. Expected : "+str(req_fields_datasource)

def check_inside_list(val,inside_fields,io):
   data_types = ['INTEGER', 'DECIMAL', 'FLOAT', 'CHAR', 'VARCHAR(100)', 'TEXT', 'DATE', 'TIME', 'TIMESTAMP', 'BOOLEAN','DATETIME','INT','DOUBLE']
   for i in val:
    req_fields=inside_fields.copy()
  
    for key,value in i.items():   
      if(key in req_fields.keys()):
        if(type(value)==req_fields[key]):
         if(key=='type'):
           if(value.upper() in data_types):
              req_fields.pop(key)
             
              continue
           else:
               return str(key)+" : "+str(value)+" ERROR. Unsupported datatype. Expected : "+str(data_types)
   
         else:
              req_fields.pop(key)
            
              continue
        elif(req_fields[key]=='dontCare'):
          req_fields.pop(key)
         
          continue
        else:
          return str(key)+" : "+str(value)+" in \'field\' has wrong format"
      else:
        return str(key)+" : "+str(value)+" in \'field\' doesn't belong to the template"

    do=list(req_fields.keys())
    dop=list(io.keys())
    check =  all(item in dop for item in do)
    if( not bool(req_fields) or check):
      continue
    return "All the parameters for \'fields\' is not provided" 

   return "V"  

def check_for_fields2(data):
    template_name=check_details(data)
    if(not check_template_exits(template_name,"DATASOURCE_TEMPLATES")):
        return "Template not found"
    working_folder = os.getcwd()
    filename = os.path.join(working_folder,"RESTAPI", "DATASOURCE_TEMPLATES",template_name+".json")

    with open(filename, 'r') as file:
            dat = json.load(file)
    type_order=[]
    for i in dat[0]['fields']:
       type_order.append(i['type'])
    
    if(len(data[0]['fields'])!=len(type_order)):
       return "Value missing/misfitting Error. Datasource template has "+str(len(type_order))+" columns, but recieved "+str(len(data[0]['fields']))+" columns. Expected columns types are : "+str(type_order)
    
    for k in data[0]['fields']:
       if("value" in k.keys() and len(k)==1): 
          continue  
       else:
          return "Key Error. Fields of Insert template doesn't match with the datasource template. Expected : "+str(dat)
       
    count=0
    for j in data[0]['fields']:
       c=validate_sql_data_type(type_order[count].upper(),j['value'])
       if(c==True):
        count+=1
        continue
       elif(c==False):
          return str(j['value'])+" doesn't match with "+ str(type_order[count])
       else:
          return c
    return 1 
       
###################


################### CHECK DATABASE FOR TEMPLATE

def check_details(data):
  for i in data:
     for key,val in i.items():
       if(key=="name"):
         template_name=val.lower()
         break
  return template_name        

def check_template_exits(names,location):
 working_folder = os.getcwd()
 file_path = os.path.join(working_folder,"RESTAPI", location,names+".json")
 files = glob.glob(file_path)
 return len(files) > 0 
 
def match_template_fields(name,data):
  working_folder = os.getcwd()
  module_name = os.path.join(working_folder,"RESTAPI", "DATASOURCE_TEMPLATES",name+".json")
  with open(module_name, 'r') as file:
            dat = json.load(file)
  
  
  fields = dat[0]['fields']
  template_values = [field['name'] for field in fields]
  fields2 = data[0]['fields']
  insert_values = [field['name'] for field in fields2]
  temp_diff = [x for x in template_values if x not in insert_values]
  insert_diff = [x for x in insert_values if x not in template_values]

  
  if(len(temp_diff)==0):
    if(len(insert_diff)==0):
      l=check_types(fields,fields2)
      if(l==1):
         return 1
      else:
         return l
    else:
      return "Some Column(s) in insert template is/are not in datasource template. Expected fields : "+str(fields)

  if(len(insert_diff)!=0):
       return str(insert_diff)+" in insert template is/are not in datasource template. Expected fields : "+str(fields)
  for remain in temp_diff:
   for i in fields:
     if(i["name"]==remain):
       if("isEmpty" in i):
         if(i["isEmpty"]==True):
           continue    
         else:
           return "Column value(s) is/are missing. Expected fields : "+str(fields)      
       else:
         return "Column value(s) is/are missing.Expected fields : "+str(fields)  

  return 1     

###################


################### VALIDATES TYPES

def check_types(fields,fields2):
  template_dict = {field['name']: field['type'] for field in fields}
  insert_dict = {field['name']: field['value'] for field in fields2}

  for key,val in template_dict.items():
     insert_value=insert_dict[key] 
     c=validate_sql_data_type(val.upper(),insert_value)
     if(c==True):
        continue
     elif(c==False):
        return str(insert_value)+" needs to have "+str(val.upper())+" datatype" 
     else:
        return c
  return 1  

def validate_sql_data_type(data_type, value):
  
  try:  
    if data_type in ['INTEGER','INT']:
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    elif data_type == 'DECIMAL':
        decimal_pattern = r'^[-+]?\d+(\.\d+)?$'
        if(re.match(decimal_pattern, str(value)) !=None):
          return True
        else:
           return False
    
    elif data_type == 'FLOAT':
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    elif data_type == 'CHAR':
        return isinstance(value, str) and len(value) == 1
    
    elif data_type == 'VARCHAR(100)' or data_type == 'TEXT':
        return isinstance(value, str)
    
    elif data_type == 'DATE':
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if(re.match(date_pattern, value) != None):
          return True 
        else:
           return False
        
    elif data_type == 'TIME':
        time_pattern = r'^\d{2}:\d{2}:\d{2}$'
        if(re.match(time_pattern, value) !=None):
           return True
        else:
           return False
    
    elif data_type == 'TIMESTAMP' or data_type=='DATETIME':
        timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        if(re.match(timestamp_pattern, value)!=None):
           return True
        else:
           return False
    
    elif data_type == 'BOOLEAN':
        return value.lower() in ['true', 'false']

    elif data_type == 'DOUBLE':
            try:
                float(value)
                return True
            except ValueError:
                return False 
    
    # Handle unknown data types
    else:
        return False
  except Exception as e:
     return "Format Error. "+str(value)+" should be wrapped around \' \' ."
###################


################### PREDICT / TRAINING PHASE
def train_predict_name(save_name,check_name):
       working_folder = os.getcwd()
       directory = os.path.join(working_folder,"RESTAPI", "TRAINING_TEMPLATES")
      #  directory ="C:/Users/sakkt/OneDrive/Documents/jana/MODULES/RESTAPI/TRAINING_TEMPLATES"  # Replace with the actual directory path
       # Get all the files in the directory
       file_list = os.listdir(directory)
       
       # Iterate over the files
       for file_name in file_list:
           file_path = os.path.join(directory, file_name)
           
           # Check if the file is a regular file
           if os.path.isfile(file_path):
               # Open the file and read its contents as JSON
               with open(file_path, 'r') as file:
                   try:
                       json_data = json.load(file)
                       if save_name==json_data[0]['name'] and check_name==json_data[0]['datasource']:
                            return True,0
                        
                   except Exception as e:
                       return False ,"JSON ERROR"    
       
       return False, " Training Template with same name and datasource not found."               

def check_predict(data,mode):
  check_name=""
  save_name=""
  save_type=""
  out=["templateVersion","type","name","datasource","selector","condition","group","sort"]
  data=data[0]
  for key,val in data.items():
    if(key in out):
      if(key=='datasource'):
         check_name=val.lower()
         data['datasource']=data['datasource'].lower()
      elif(key=='name'):
         data['name']=data['name'].lower()
         save_name=val.lower() 
      elif(key=='type'):
         save_type=val
         if((val.lower()=='training' and mode==0) or (val.lower()=='prediction' and mode==1)):
            pass
         else:
            if(mode==0):
              return 'Value Error. The uploaded file is of type : Prediction. Expected type : Training for request_service : 12 '
          
            if(mode==1):
              return 'Value Error. The uploaded file is of type : Training. Expected type : Prediction for request_service : 13 '
          
      out.remove(key)
    else:
      if(mode==0 and key in ['predict','window','horizon']):
         continue
      return str(key)+" not in template"
 
  if(mode==0):
     for i in ['predict','window','horizon']:
      if(i not in data.keys()):
        return  " Key Error. Window, Horizon and Predict keys are required for training template."
  if(len(out)==0):
    return " Key Error. Only group or condition must be in the template"
  elif(len(out)>1):
      return " Key Error. Missing keys in templates : "+str(out)
  elif((len(out)==1 and "condition" in out) or (len(out)==1 and "group" in out)):
     for val in out:
        excep=val
     pass
  
  g1=check_template_exits(check_name,"DATASOURCE_TEMPLATES")
  if(g1 is False):
    return "You must create a datasouce template before training it"
  
  if(mode==1):
    
    g,msg=train_predict_name(save_name,check_name)
    if(not g):
       return msg
      

  working_folder = os.getcwd()
  module_name = os.path.join(working_folder,"RESTAPI","DATASOURCE_TEMPLATES",check_name+".json")
  with open(module_name, 'r') as file:
            dat = json.load(file)
  
  fields = dat[0]['fields']
  template_values = [field['name'] for field in fields]

  selector_fields={"fields":list,"action":str}
  a1=check_selector(data["selector"],template_values,selector_fields,0)
  if(a1!="V1"):
    return a1
  

  main_field=['name','field','match','value']
  if(excep =='group'):
     a2=check_condition(data["condition"],check_name,template_values,main_field,0)
     if(a2!="V2"):
       return a2
  else:
     a3=check_group(data["group"],check_name,template_values)
     if(a3!="V3"):
       return a3
  
  a4=check_sort(data["sort"],template_values)
  if(a4!="V4"):
    return a4
  
  if(mode==0):
     a5=check_horizon(data["window"],data['horizon'],data['predict'],template_values)
     if(a5!="V5"):
        return a5
      
  return True,save_type,save_name

###################


################### SELECTORS
def check_selector_fields(data,template_values,addr):
  template_values_copy=template_values.copy()
  for i in data:
    if(len(i)==1 and "name" in i.keys()):
      if(type(i["name"]) is str):
        if(i["name"] in template_values_copy):
          template_values_copy.remove(i["name"])
        else:
          return "Key Error in NAME field of "+addr+". "+"\'"+str(i["name"])+"\' column does not belong the column of the specified datasource. Expected Columns : "+str(template_values)
      else:
        return "Type Error in NAME field of "+addr+". Expected string type for NAME field"    
    else:
      return "Key Error in the Fields of "+addr+". Only NAME field is expected inside the fields of "+addr
  return 1  

def check_selector(data,template_values,selector_fields,call):
  addr=''
  if call==0:
    addr='SELECTOR'
  elif call==1:
    addr='GROUP'
  elif call==2:
    addr='SORT'  
  
  for i in data:
    for key,pair in i.items():
      if key in selector_fields.keys():
        if type(pair) == selector_fields[key]:
           selector_fields.pop(key)
           
           
        else:
          return "Format error in "+addr+". \'"+str(key)+"\' is expected to have " +str(selector_fields[key])+" type"
      else:
        return "Key error in "+addr+". \'"+str(key)+"\' key doesn't belong to "+addr+" field" 
     
    
  operations = ["unique",""," ","maximum", "minimum", "average", "total", "count","distinct","sum"]
  order=['ascending','descending']
  if(len(selector_fields)==0 or (len(selector_fields)==1 and "action" in selector_fields.keys() )):
         
         for i in data:
           for key,val in i.items():
             if(key=='fields'):

               if(len(val)>0):
                 a=check_selector_fields(val,template_values,addr)
                 if(a == 1):
                   continue
                 else:
                   return a
               else:
                   return "Format error in Fields of "+addr+" ."+ "Expected:One or More Name key inside the fields of "+addr
             elif(key=='action'):
                if(call==0): 
                   if(val.lower() in operations):
                     continue
                   else:
                     return "Value error in Action of "+addr+". \'"+str(val)+"\' is not a valid action. Expected actions : "+str(operations)
                elif(call==2):
                  if(val.lower() in order):
                     continue
                  else:
                     return "Value error in Action of "+addr+". \'"+str(val)+"\' is not a valid action. Expected actions : "+str(order)
                else:
                  continue

         return "V1"       

    
  else:
      return str(selector_fields.keys())+" is/are missing in selector field"
###################      

      

################### CONDITIONS

def check_keys_in_dictionary(keys, dictionary):
    for key in keys:
        if key not in dictionary or len(dictionary)!=len(keys):
            return False
    return True

def check_inner_condition(dictionary,template_dict,template_values,match,condition_names,call,addr):
  between_types = ['INT', 'INTEGER', 'SMALLINT', 'BIGINT', 'FLOAT', 'DOUBLE', 'DOUBLE PRECISION', 'DECIMAL', 'NUMERIC', 'DATE', 'TIME', 'DATETIME', 'TIMESTAMP']
  check=False
  if(dictionary["field"] in template_values):
    if dictionary['match'].lower() in match:
      if(dictionary['match'].lower()=='between'):
        if(type(dictionary['value'])==list):
            if(len(dictionary['value'])==2):
               if(template_dict[dictionary['field']].upper() in between_types):
                 for i in dictionary['value']:
                    
                    c=validate_sql_data_type(template_dict[dictionary['field']].upper(),i)
                    if(c==True):
                       check=True   
                    elif(c==False):
                       return condition_names,"Type Error in Value Field of \'"+ str(dictionary['name'])+"\' condition of "+addr+" Field. Expected "+str(template_dict[dictionary['field']])+" Datatype for "+str(dictionary['field'])
                    else:
                       return condition_names,c
               else:
                  
                  return condition_names,"Type Error in Value Field of \'"+ str(dictionary['name'])+"\' condition of "+addr+" Field. Expected \'Between\' Match only for "+str(between_types)
            else:
              return condition_names,"Value Error in VALUE field of \'"+ str(dictionary['name'])+"\' condition of "+addr+" Field. Expected value = [min_bound,max_bound] for match=\'between\'"
        else:
           return condition_names,"Type Error in VALUE field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. Expected type is a \'list\' eg: [min_bound,max_bound] for match=\'between\'"      
      else:
          if(type(dictionary['value'])!=list):
           if(dictionary['field'] in template_dict.keys()):
            c=validate_sql_data_type(template_dict[dictionary['field']].upper(), dictionary['value'])
            if(c==True):
              check=True
            elif(c==False):
               return condition_names,"Type Error in VALUE field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. Field => "+str(dictionary['field'])+" : "+str(dictionary['value'])+" .Expected type : "+ str(template_dict[dictionary['field']].upper())  
            else:
               return condition_names,c
          else:
             return condition_names,"Type Error in VALUE field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. Expected a value of specified Datatype not a list"  

    else:
        return condition_names,str("Value Error in MATCH field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. Expected match values are : "+str(match))
  else:
    return condition_names,str("Value Error in FIELD of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. \'"+dictionary['field'])+"\' column doesn't belong to the datasource template. Columns in datasource templates are : "+str(template_values)  

 
  if(call!=0):
    conditions=['unique','',' ','distinct','maximum','minimum','average','total', 'count','sum']
    if(dictionary['aggregation'].lower() in conditions):
      pass
    else:
      return condition_names,"Type Error in AGGREGATION field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. \'"+dictionary['aggregation']+"\' not valid. Expected aggregation : '"+str(conditions)


  if dictionary['name'] not in condition_names:
        condition_names.append(dictionary['name'])
        return condition_names,1
  else: 
        return condition_names,"Value Error in NAME field of \'"+str(dictionary['name'])+"\' condition of "+addr+" Field. \'+"+dictionary['name']+"\' has duplicates. Expected unique NAME FIELDS"

def is_balanced(code,name,addr):
    stack = []
    opening_brackets = {'(', '[', '{'}
    closing_brackets = {')', ']', '}'}
    bracket_pairs = {'(': ')', '[': ']', '{': '}'}
    action=['or','and']
    skip=-1
    count=0
    ac=0
    wait_or=False
    def get_substring(string, index):
       substring = ""
       length = len(string)
       
   
       while index < length:
           char = string[index]
           if char.isspace() or char in closing_brackets or char in opening_brackets:
               break
           substring += char
           index += 1
      
       if(substring in name):
           if(not wait_or):
             return True,index-1,1
           else:
               return False,0,"Format Error in Action field of "+addr+". Before "+substring+" a condition [OR,AND] is expected."
       elif(substring.lower() in action):
           if(wait_or):           
            return True,index-1,0
           else:
               return False,0,"Format Error in Action field of "+addr+". Two conditions [OR,AND] cannot follow up"
           
       else:
           return False,0,"Value Error in Action field of "+addr+". "+substring+" not found in given conditions."
       

          

    ignore_space = False
    variable = ''
    for i,char in enumerate(code):
        if(i<=skip):
            continue
        if ignore_space and char == ' ':
            continue
        if char == ' ':
            ignore_space = True
            continue
        ignore_space = False

        if char in opening_brackets and wait_or==False:
            stack.append(char)
            count=0
            ac=0
            wait_or=False
        
               
        elif char in closing_brackets:
            if not stack or bracket_pairs[stack.pop()] != char or wait_or==False or count<=0 or ac<=0:
                if(wait_or==False):
                   return "Format Error in Action field of "+addr+". Expected a condition name before closing bracket not [AND, OR]"
                if(count<=0):
                   return "Format Error in Action field of "+addr+". Null brackets not allowed .Expected a value inside brackets"
                if(ac<=0):
                   return "Format Error in Action field of "+addr+". (condition name) not allowed. Expected atleast a operation inside the brackets. "
                return "Brackets not balanced"
            wait_or=True
        elif char.isalpha() or char.isdigit():
            
            
            status,v,wait=get_substring(code,i)
            
            if(status):
                skip=v
                if(wait):
                    wait_or=True
                    count+=1
                else:
                    wait_or=False   
                    count+=1
                    ac+=1 
                

            else:
                return wait   
        else:
            return False  

    return "1" if len(stack) == 0 else "Brackets not balanced"


           
#action format
def check_condition_action(dictionary,condition_names,addr):
  if isinstance(dictionary['action'],list):
    string = dictionary['action'][0]
     
    
    #check for bracket balancing
    #############
    status=is_balanced(string,condition_names,addr)
    if(status=="1"):
        return 1
    #############
    else:
       return status
  else:
     return "Type Error in Action Field. Expected type : List"

def check_condition(data,check_name,template_values,main_field,call): 
  addr=''
  if call==0:
    addr='CONDITION'
  elif call==1:
    addr='GROUP'
  
  working_folder = os.getcwd()
  filename = os.path.join(working_folder,"RESTAPI", "DATASOURCE_TEMPLATES",check_name+".json")
  with open(filename, 'r') as file:
            dat = json.load(file)
  
  fields = dat[0]['fields']
  template_dict = {field['name']: field['type'] for field in fields}


  

  main=0
  action=0
  match = ["equal", "notequal", "greaterthan", "lessthan", "greaterthanorequal", "lessthanorequal", "between", "startwith", "endwith", "contains"]
  condition_names=[]
  
  for dictionary in data:
    
    if(check_keys_in_dictionary(main_field,dictionary)):
      main+=1
      condition_names,valid=check_inner_condition(dictionary,template_dict,template_values,match,condition_names,call,addr)
      
      if(valid==1):
        continue
      else:
        return valid
    elif(check_keys_in_dictionary(['action'],dictionary)):
      a=check_condition_action(dictionary,condition_names,addr)
      if(a!=1):
         return a
      action+=1
      continue
    else:
      return "Key Error in "+addr+" Field. "+str(dictionary)+" doesn't match with the expected keys. Expected keys : "+str(main_field)
 
  if(action>1):
    return "Key Error in ACTION field of "+addr+" Field. "+"Expected: One action field in condition. Passed "+str(action)+" actions"
  if(main<1):
    return "Key Error in "+addr+" Field.  Passed "+str(main)+" condition. Expexted: One or More condition."
 
  else:
    return "V2"

###################




################### GROUP

def check_group(data,check_name,template_values):

  selector_fields={"fields":list,"condition":list,"action":list}
  a=check_selector(data,template_values,selector_fields,1)
  if(a!="V1"):
    return a
  for i in data:
    for key,value in i.items():
      if key=='condition':
        val=value
  main_field=['name','field','match','value','aggregation']
  b=check_condition(val,check_name,template_values,main_field,1)
  if(b=='V2'):
    return 'V3'
  return b

###################  



################### SORT

def check_sort(data,template_values):

  selector_fields={"fields":list,"action":str}
  a=check_selector(data,template_values,selector_fields,2)
  if(a!="V1"):
    return a
  return "V4"
  ######################
  
###################


################### WINDOW, HORIZON, PREDICT

def check_horizon(win,hor,predict,template_values):
   if(type(win)==int):
      if(type(hor)==int):
         pass
      else:
         return "Value Error in Horizon field. Expected a integer value for horizon"
   else:
         return "Value Error in Window field. Expected a integer value for window"
   
   if not predict in template_values:
      return "Value Error in Predict field. "+predict+" not in datasource Template. Expected Predict fields are "+str(template_values)
      
   return "V5"
   
###################
       

