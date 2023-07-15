import json
import yaml
import os
import importlib.util


   
def createTemplate(file):
  try:
     a=check_file(file.filename)
     return str(a)
  except Exception as e:
       return "ERROR : FILE NOT FOUND"

def modifytemplate():
     return 'under developement' 
          
   
def Training_sub(mode,num=-1):
    working_folder = os.getcwd()
    
    if(mode=='training'):
        location="TRAINING_TEMPLATES"    
    elif(mode=='prediction'):
        location="PREDICTION_TEMPLATES"
    else:
        location='DATASOURCE_TEMPLATES'     
    file_path = os.path.join(working_folder,"RESTAPI",location)  
    files_in_dir={}
    count=0
    for root, dirs, files in os.walk(file_path):
          for file in files:
              files_in_dir[count]=file
              count+=1
    if(num==-1):          
      return files_in_dir
    if(num==-2):
        return "VALUE MISSING ERROR. Missing template number for train/pred. Expected num = 0,1 for training/prediciton respectively"  
   
    elif(int(num) in files_in_dir.keys()):
        sel_file=files_in_dir[int(num)]
        file_name = os.path.join(working_folder,"RESTAPI",location,sel_file)  
        with open(file_name, 'r') as file:
          dat = json.load(file)
        return dat   
    else:

        return "File not Found Error. Keys found: "+str(files_in_dir.keys())

def Train_Pred(mode,temp_num):
    if(mode=="training" or mode=="prediction"):   
       files_in_dir=Training_sub(mode,temp_num)
       if(type(files_in_dir)!=list):
           return files_in_dir
       else:
           res=PASS_TO_QP(files_in_dir,mode)
           return res
    else:
        return "Value Error. Types accepted are 'training' for Training and 'prediction' for Predictions"
     

               

def PASS_TO_QP(data,mode):
    
    working_folder = os.getcwd()
    module_name = os.path.join(working_folder,"QUERY_PARSE", "CIP")
    spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
    module2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module2)
    response_from_qp=module2.tp_qp_connector(data,mode)
    return response_from_qp



def check_file(file_path):
    # Check file extension  
    if file_path.endswith(".json"): 
        return 1
    elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
        return 1
    try:
    # Check file content
          with open(file_path, "r") as file:   
        
            json.loads(file.read())
            return 1
    except Exception as e:
            pass
    try:
         with open(file_path, "r") as file:
        
            yaml.safe_load(file)
            return 1
    except Exception as e:
            pass
 
    return 0
       