__author__ = "Jaya Sri Krishna S"
__email__ = "jayasri.krishnas2020@vitstudent.ac.in"
__status__ = "Production"
import importlib.util
from RESTAPI.services import *
import os
from fastapi import FastAPI, Request
from urllib.parse import quote
import json
from fastapi.responses import PlainTextResponse
from typing import Union
import json
from fastapi import UploadFile, File 
app = FastAPI()
working_folder = os.getcwd()

module_name = os.path.join(working_folder,"TEMP_PARSE", "Temp_parser")
spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
template_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template_parser)


module_name = os.path.join(working_folder,"CONNECTOR", "my_mindsdbconnector")
spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
connector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connector)
 

module_name = os.path.join(working_folder,"NGROK", "ngrok")
spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
ngrok = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ngrok)

ngrok.establish()


@app.get("/")
async def root():
    return {"message": "Server is up and running"}


@app.get("/show_services", response_class=PlainTextResponse)
async def show_services():
    ret_value = '1:"createTemplate"\n  create_temp => datasource Template\n  training_temp => training Template\n  prediction_temp => Prediction Template\n\n"modify" => "modifyTemplate"\n\n"insert_temp":"insertData"\n\n"training" => "Training"\n\n"prediction" => "Prediction"'
    return ret_value


@app.get("/show_templates")
async def templates(types: str = '', template_id: int = -1):
    if (str(types) == 'training' or str(types) == 'prediction' or str(types) == 'datasource'):
        pass
    else:
        return "Key Error. Accepted types types=training,prediction"

    s = Training_sub(str(types), template_id)
    return s


@app.post("/choose_service")
async def services(request_service: str = '', file: UploadFile = File(None), template_id: int = -2):
    create = ['datasource_template', 'training_template',
              'prediction_template', 'insert_template']
    if (request_service in create):
        s = createTemplate(file)
        if (s == "1"):
            try:
                file_name = file.filename
                if (file_name.endswith(".json")):
                    contents = await file.read()
                    data = json.loads(contents)

                else:
                    contents = await file.read()
                    yaml_str = contents.decode("utf-8")
                    yaml_dict = yaml.safe_load(yaml_str)
                    json_str = json.dumps(yaml_dict, indent=4)
                    data = json.loads(json_str)

            except Exception as e:
                return "File Error. Format is wrong. check for missing \" \" ,() and [] "
            a = template_parser.parser(data, request_service)
            if (a == "1"):
                #return a
                #  pass to qp
                if request_service not in ['prediction_template', 'training_template']:
                    res = PASS_TO_QP(data, request_service)
                    if res!=1 and request_service=='datasource_template':
                        file_path = os.path.join(working_folder,"RESTAPI", request_service.upper()+"S",data[0]['name']+".json")
                        try:
                          os.remove(file_path)
                        except Exception as e:
                          pass  
                    return res
                return (a) 
            else:
                return a
        elif (s == "0"):
            return {"ERROR": "ONLY JSON AND YAML ARE ACCEPTED"}
        else:
            return {"INTERNAL ERROR. "+s}

    if (request_service == 'modify'):
        s = modifytemplate()
        return s

    if (request_service == 'training'):
        types = 'training'
        s = Train_Pred(types, template_id)
      
        return str(s)
        # res=PASS_TO_QP(s,12)
        # return (res)

    if (request_service == 'prediction'):
        types = 'prediction'
        s = Train_Pred(types, template_id)
        return s

    else:
        return {"status": "invalid service"}


@app.get("/check_status", response_class=PlainTextResponse)
async def status(template_id: int = -1):
    if (template_id < 0):
        return "Expecting a template id"

    s = Training_sub('training', template_id)
    # return(s[0]['name'])
    res = connector.status(s[0]['name'].lower())
    return (res)
   # send to CONNECTOR return s[0]['name']


