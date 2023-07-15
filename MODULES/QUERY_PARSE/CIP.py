import mysql.connector
from MySQLdb.converters import conversions
import importlib.util 
import datetime
import os

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# MySQL Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Connect to MySQL
connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,

    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)



def create_table(x):
    try:
        cursor = connection.cursor()
        for item in x:
            if 'type' in item:
                tablename=[]
                tablename=item['name']
                create_table_query = f"CREATE TABLE IF NOT EXISTS {tablename} ("
                colnames = []
                coltypes= []
                for item in x:
                    if 'fields' in item:
                        for field in item['fields']:
                            if 'name' in field:
                                colnames.append(field['name'])
                            if 'type' in field and 'isEmpty' in field:
                                combined=str(field['type'])+" "+"NOT NULL"
                                coltypes.append(combined)
                            else:
                                coltypes.append(field['type'])
                for i in range(len(colnames)):
                    column_name = colnames[i]
                    column_type = coltypes[i]
                    
                    create_table_query += f"{column_name} {column_type} ,"
                create_table_query = create_table_query.rstrip(", ")

                create_table_query += ")"
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()
     
        return(1)
    except Exception as e:
        return(e)
        

def insert_table(x):
    try:
        cursor = connection.cursor()
        for item in x:
            if 'type' in item:
                tablename=[]
                tablename=item['name']
                query = f"SHOW COLUMNS FROM {tablename}"
                cursor.execute(query)
                column = cursor.fetchall()
                columns = [column[0] for column in column]
                values=item['fields']
                row_values = tuple([item['value'] for item in values])
                insert_query = "INSERT INTO {} ({}) VALUES ({})".format(
                    tablename,
                    ', '.join(columns),
                    ', '.join('%s' for _ in columns)
                )
                x1=len(columns)


                result=[]
                for i in range(0, len(row_values), x1):
                    tuple_elements = row_values[i:i+x1]
                    result.append(tuple(tuple_elements))
                cursor.executemany(insert_query,result)
                print(insert_query)
        connection.commit()
        cursor.close()
        connection.close()
        return(1)
    except Exception as e:
        return(e)
    
# "C:\Users\sakkt\OneDrive\Documents\jana\MODULES\CONNECTOR\my_mindsdbconnector.py"
def training_table1(x):
    try:
        
        working_folder = os.getcwd()
        module_name = os.path.join(working_folder,"CONNECTOR", "my_mindsdbconnector")
        spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
        connector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(connector)
        
        cursor = connection.cursor()
        
        # Access the values
        template_version = x[0]['templateVersion']
        training_type = x[0]['type']
        tablename = x[0]['datasource']
        name=x[0]['name']
        selector_fields = x[0]['selector'][0]['fields']
        selector_action = x[0]['selector'][1]['action']
        condition=x[0]['condition']
        sort=x[0]['sort']
        sort_fields=x[0]['sort'][0]['fields']
        sort_action=x[0]['sort'][1]['action']
        if training_type.lower() =='training':
            predictor=x[0]['predict']
            windows=x[0]['window']
            horizon=x[0]['horizon']
        

        column=[]
        for item in selector_fields:
            if isinstance(item, dict):
                for key,value in item.items():
                    if 'all' not in value:
                        column.append(value)
                        break
                    else:
                        column.append('*')


            
        condition_field=[] 
        condition_match=[]
        condition_value=[] 
        condition_name=[] 
        action=[]         
        for item in condition:
            if isinstance(item, dict):
                for key, value in item.items():
                    if key=='field':
                        condition_field.append(value)
                    elif key=='match':
                        condition_match.append(value)
                    elif key=='value':
                        if isinstance(value,list):
                            condition_value.append(value)
                        else:
                            condition_value.append(value)
                    elif key=='name':
                        condition_name.append(value)
                    elif key=='action':
                        action=value
        # print(condition_value)
        condition_value= [f"'{item}'" if isinstance(item, str) else str(item) for item in condition_value]
        # print(condition_value)

        if isinstance(action,list):
            if len(action)!=0: 
                string = action[0]
                split_list = string.split(" ")
                condition_action = [item.strip() for item in split_list]
            else:
                condition_action=[]
        else:
            condition_action=[]

        count=len(condition_name)
        
        if selector_action.lower()=='unique' or selector_action.lower()=='distinct':
            s_action='DISTINCT'
        elif selector_action.lower()=='maximum' or selector_action.lower()=='max':
            s_action='MAX'
        elif selector_action.lower()=='minimum' or selector_action.lower()=='min':
            s_action='MIN'
        elif selector_action.lower()=='average' or selector_action.lower()=='avg':
            s_action='AVG'
        elif selector_action.lower()=='total' or selector_action.lower()=='sum':
            s_action='SUM'
        elif selector_action.lower()=='count':
            s_action='COUNT'
        else:
            s_action=" "

        match=[]
        for i in range (0,count):
            if condition_match[i].lower() =='equal':
                match.append('=')
            elif condition_match[i].lower() =='notequal':


                match.append('<>')
            elif condition_match[i].lower() =='greaterthan':
                match.append('>')
            elif condition_match[i].lower() =='lessthan':
                match.append('<')
            elif condition_match[i].lower() =='greaterthanorequal':
                match.append('>=')
            elif condition_match[i].lower() =='lessthanorequal':
                match.append('<=')
            elif condition_match[i].lower() =='between':
                match.append('BETWEEN')
            elif condition_match[i].lower()=='startwith':
                match.append('{}%')
            elif condition_match[i].lower() =='endwith':
                match.append('%{}')
            else:
                print('error')
            
        condition=[]
        s=[]
        s.append('WHERE')
        for i in range (0,count):
            s.append(condition_field[i])
            if match[i]=='BETWEEN':
                s.append(match[i])
                s.append("{} and {}".format(condition_value[i][0], condition_value[i][1]))
            elif match[i]=='{}%':
                s.append("LIKE {}".format(match[i].format(condition_value[i])))
            elif match[i]=='%{}':
                s.append("LIKE {}".format(match[i].format(condition_value[i])))
            else:
                s.append(match[i])
                s.append(condition_value[i])
            condition.append(s)
            s=[]
            

        # print(condition)
        if isinstance(action,list):
            if len(action)!=0:
                if len(condition_action)%2==0:
                    c_action=[]
                    for i in range(1,count+2,2):
                        c_action.append(condition_action[i])
                else:
                    c_action=[]
                    for i in range(1,count+1,2):
                        c_action.append(condition_action[i])

            else:
                c_action=condition_action
            # print(c_action)
        else:
            c_action=condition_action


        result1 = [' '.join(str(element) for element in inner_list) for inner_list in condition]
        # print(result1)
        result = [val for pair in zip(result1, c_action + ['']) for val in pair if val]

        so_field=[]
        for item in sort_fields:
            if isinstance(item,dict):
                for key,value in item.items():
                    if 'name' in key:
                        so_field.append(value)
        so_action=[]
        if isinstance(sort_action,list):
            for item in sort_action:
                    if item.lower()=='ascending' or item.lower()=='asc':
                        so_action.append("ASC")
                    elif item.lower()=='descending' or item.lower()=='desc':
                        so_action.append('DESC')
                        
        elif isinstance(sort_action,str):
                if sort_action.lower()=='ascending' or sort_action.lower()=='asc':
                    so_action.append("ASC")
                elif sort_action.lower()=='descending' or sort_action.lower()=='desc':
                    so_action.append("DESC")


        sa=[]
        for i in range(0,len(so_field)):
            sa.append(so_field[i])
            sa.append(so_action[i])


        ssa = []
        for i in range(len(sa)):
            ssa.append(sa[i])
            if (i + 1) % 2 == 0 and i < len(sa) - 1:
                ssa.append(',')

        if training_type.lower()=='training':
            if "DISTINCT" in s_action or " "in s_action or '' in s_action:
                query = "SELECT {} {} FROM {} {} ORDER BY {};".format(s_action,", ".join(column), tablename," ".join(result)," ".join(ssa))
            else:
                query = "SELECT {} ({}) FROM {} {} ORDER BY {};".format(s_action,", ".join(column), tablename," ".join(result)," ".join(ssa))
            print(query)

            cursor = connection.cursor()
            cursor.execute(query)
            results=cursor.fetchall()
            # print(results)
            column_names1 = [column[0] for column in cursor.description]
            # print(column_names1)
            # column_types = [conversions.get(column[1], str) for column in cursor.description]
            column_types = [conversions.get(column[1], str).__name__ for column in cursor.description]
            for i in range(len(column_types)):
                if column_types[i]=='bytes':
                    column_types[i]='text'
                elif column_types[i].lower()=='datetime_or_none':
                    column_types[i]='datetime'
            
            create_table_query = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join([f'{name} {dtype}' for name, dtype in zip(column_names1, column_types)])})"
            print(create_table_query)
            cursor.execute(create_table_query)
            insert_query = f"INSERT INTO {name} ({', '.join(column_names1)}) VALUES ({', '.join(['%s'] * len(column_names1))})"
            formatted_results = []

            for row in results:
                formatted_row = []
                for value in row:
                    if isinstance(value, datetime.datetime):
                        formatted_value = value.strftime('%Y-%m-%d %H:%M:%S')
                        formatted_row.append(formatted_value)
                    else:
                        formatted_row.append(value)
                formatted_results.append(tuple(formatted_row))
            # print(formatted_results)
            # cursor.executemany(insert_query, formatted_results)
            try:
                cursor.executemany(insert_query, formatted_results)
                connection.commit()  # Make sure to commit the changes
            except Exception as e:
                print("Error occurred while inserting data:", str(e))
            # connection.commit()
            # csv_value=[] 
            # for row in results:
            #     for value in row:
            #         csv_value.append(value)
            
            
            # def convert_csv(csv_value):
            #     csv_data = [csv_value[i:i+len(column_names1)] for i in range(0, len(csv_value), len(column_names1))]
                
            #     csv_file_path = 'C:/Users/sakkt/OneDrive/Documents/jana/{}.csv'.format(name)
            #     with open(csv_file_path, 'w', newline='') as file:
            #         writer = csv.writer(file)
            #         writer.writerow(column_names1)
            #         writer.writerows(csv_data)
            #         print("CSV file created successfully.")
                    

            
                # if training_type.lower()=='training':
                #     convert_csv(csv_value)
            column_names2=[]
            for column in column_names1:
                if predictor not in column:
                    column_names2.append(column)
            print(column_names2)
            qx=[]
            qx=[name,name,predictor,column_names1[0],column_names2[1:],windows,horizon]
            print(qx)
            
            return(connector.train(qx))
        
            
        elif training_type=='prediction':
            column1=column.copy()
            column1[0]='date'
            print(column)
            pc = ', '.join(['m.{} as {}'.format(x, y) for x, y in zip(column, column1)])
            if "DISTINCT" in s_action or " "in s_action or '' in s_action:
                query = "SELECT * FROM (SELECT {}{} FROM mindsdb.{} as m JOIN mysql_datasource.{} as t WHERE t.{} > LATEST)  {} ORDER BY {} {};".format(s_action,pc, name,name,column[0]," ".join(result),column1[0]," ".join(ssa[1:]))
            else:
                query = "SELECT * FROM (SELECT ({}){} FROM mindsdb.{} as m JOIN mysql_datasource.{} as t WHERE t.{} > LATEST) {} ORDER BY {};".format(s_action,pc, name,name,column[0]," ".join(result)," ".join(ssa))
            print(query)
            return(connector.prediction_m(query))
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(e)  
        return(e)
        
                  
           

def training_table2(x):
    # try:
    cursor = connection.cursor()
    template_version = x[0]['templateVersion']
    training_type = x[0]['type']
    tablename = x[0]['datasource']
    name=x[0]['name']
    selector_fields = x[0]['selector'][0]['fields']
    selector_action = x[0]['selector'][1]['action']
    group_condition=x[0]['group'][1]['condition']
    group_fields1=x[0]['group'][0]['fields']
    group_act=x[0]['group'][1]['condition']
    # print(group_act)
    sort=x[0]['sort']
    sort_fields=x[0]['sort'][0]['fields']
    sort_action=x[0]['sort'][1]['action']
    print(group_fields1)
    if training_type.lower() =='training':
        predictor=x[0]['predict']
        windows=x[0]['window']
        horizon=x[0]['horizon']
    group_field=[]
    for item in group_fields1:
        for key,value in item.items():
            group_field.append(value)
    print(group_field)

    for item in group_act:
        for key,value in item.items():
            if key == 'action':
                group_action=value


    column=[]
    for item in selector_fields:
        if isinstance(item, dict):
            for key,value in item.items():
                if 'all' not in value:
                    column.append(value)
                    break
                else:
                    column.append('*')
    if isinstance(group_action,list):
        if len(group_action)!=0:
                string = group_action[0]
                split_list = string.split(" ")
                group_condition_action = [item.strip() for item in split_list]
        else:
            group_condition_action=[]
    else:
        group_condition_action=[]
    if isinstance(selector_action,str):
        if selector_action.lower()=='unique' or selector_action.lower()=='distinct':
            s_action='DISTINCT'
        elif selector_action.lower()=='maximum' or selector_action.lower()=='max':
            s_action='MAX'
        elif selector_action.lower()=='minimum' or selector_action.lower()=='min':
            s_action='MIN'
        elif selector_action.lower()=='average' or selector_action.lower()=='avg':
            s_action='AVG'
        elif selector_action.lower()=='total' or selector_action.lower()=='sum':
            s_action='SUM'
        elif selector_action.lower()=='count':
            s_action='COUNT'
        else:
            s_action=""
    elif(selector_action,list):
        s_action=[]
        for item in selector_action:
            if item.lower()=='unique' or item.lower()=='distinct':
                s_action.append('DISTINCT')
            elif item.lower()=='maximum' or item.lower()=='max':
                s_action.append('MAX')
            elif item.lower()=='minimum' or item.lower()=='min':
                s_action.append('MIN')
            elif item.lower()=='average' or item.lower()=='avg':
                s_action.append('AVG')
            elif item.lower()=='total' or item.lower()=='sum':
                s_action.append('SUM')
            elif item.lower()=='count':
                s_action.append('COUNT')
            else:
                s_action.append("")
            

    
    
    group_condition_field=[] 
    group_condition_match=[]
    group_condition_value=[] 
    group_condition_name=[]
    group_condition_aggregation=[] 
    action=[]         
    for item in group_condition:
        if isinstance(item, dict):
            for key, value in item.items():
                if key=='field':
                    group_condition_field.append(value)
                elif key=='match':
                    group_condition_match.append(value)
                elif key=='value':
                    if isinstance(value,list):
                        group_condition_value.append(value)
                    else:
                        group_condition_value.append(value)
                elif key=='name':
                    group_condition_name.append(value)
                elif key=='aggregation':
                    group_condition_aggregation.append(value)
    count=len(group_condition_name)        

    match=[]
    for i in range (0,count):
        if group_condition_match[i].lower() =='equal':
            match.append('=')
        elif group_condition_match[i].lower() =='notequal':
            match.append('<>')
        elif group_condition_match[i].lower() =='greaterthan':
            match.append('>')
        elif group_condition_match[i].lower() =='lessthan':
            match.append('<')
        elif group_condition_match[i].lower() =='greaterthanorequal':
            match.append('>=')
        elif group_condition_match[i].lower() =='lessthanorequal':
            match.append('<=')
        elif group_condition_match[i].lower() =='between':
            match.append('BETWEEN')
        elif group_condition_match[i].lower()=='startwith':
            match.append('{}%')
        elif group_condition_match[i].lower() =='endwith':
            match.append('%{}')
        
    condition=[]
    s=[]
    for i in range (0,count):
        if group_condition_aggregation[i].lower()=='unique' or group_condition_aggregation[i].lower()=='distinct':
            s.append('DISTINCT')
        elif group_condition_aggregation[i].lower()=='maximun' or group_condition_aggregation[i].lower()=='max':
            s.append('MAX')
        elif group_condition_aggregation[i].lower()=='minimun' or group_condition_aggregation[i].lower()=='min':
            s.append('MIN')
        elif group_condition_aggregation[i].lower()=='average' or group_condition_aggregation[i].lower()=='avg':
            s.append('AVG')
        elif group_condition_aggregation[i].lower()=='total' or group_condition_aggregation[i].lower()=='sum':
            s.append('SUM')
        elif group_condition_aggregation[i].lower()=='count' or group_condition_aggregation[i].lower()=='count':
            s.append('COUNT')
        elif group_condition_aggregation[i].lower()==' ' or group_condition_aggregation[i].lower()=='':
            s.append(' ')
        s.append(group_condition_field[i])
        if match[i]=='BETWEEN':
            s.append(match[i])
            s.append("{} and {}".format(group_condition_value[i][0], group_condition_value[i][1]))
        elif match[i]=='{}%':
            s.append("LIKE {}".format(match[i].format(group_condition_value[i])))
        elif match[i]=='%{}':
            s.append("LIKE {}".format(match[i].format(group_condition_value[i])))
        else:
            s.append(match[i])
            s.append(group_condition_value[i])
        condition.append(s)
        s=[]
        
    if isinstance(group_action,list):
        if len(group_action)!=0:
            if len(group_condition_action)%2==0:
                c_action=[]
                for i in range(1,count+2,2):
                    c_action.append(group_condition_action[i])
            else:
            
                c_action=[]
                for i in range(1,count+1,2):
                    c_action.append(group_condition_action[i])
        else:
            c_action=group_condition_action
    else:
        c_action=group_condition_action

    result1=[]
    for i in range(0,len(condition)):
        if condition[i][0]=='DISTINCT' or condition[i][0]==' ':
            result1.append(['{} {} {} {}'.format(condition[i][0],condition[i][1],condition[i][2],condition[i][3])])
        else:
            result1.append(['{}({}) {} {}'.format(condition[i][0],condition[i][1],condition[i][2],condition[i][3])])
    

    result2 = [element for sublist in result1 for element in sublist]
    
    result = [val for pair in zip(result2, c_action + ['']) for val in pair if val]
    
    so_field=[]
    for item in sort_fields:
        if isinstance(item,dict):
            for key,value in item.items():
                if 'name' in key:
                    so_field.append(value)
    so_action=[]
    if isinstance(sort_action,list):
        for item in sort_action:
                if item.lower()=='ascending' or item.lower()=='asc':
                    so_action.append("ASC")
                elif item.lower()=='descending' or item.lower()=='desc':
                    so_action.append('DESC')
                    
    elif isinstance(sort_action,str):
            if sort_action.lower()=='ascending' or sort_action.lower()=='asc':
                so_action.append("ASC")
            elif sort_action.lower()=='descending' or sort_action.lower()=='desc':
                so_action.append("DESC")


    sa=[]
    for i in range(0,len(so_field)):
        sa.append(so_field[i])
        sa.append(so_action[i])
    

    ssa = []
    for i in range(len(sa)):
        ssa.append(sa[i])
        if (i + 1) % 2 == 0 and i < len(sa) - 1:
            ssa.append(',')
    
    if isinstance(s_action,str):
        if "DISTINCT" in s_action or " "in s_action or "" in s_action:
            query = "SELECT {} {} FROM {}  GROUP BY {} ORDER BY {} ;".format(s_action,", ".join(column), tablename,", ".join(group_field)," ".join(ssa))
            print(s_action)
        else:
            query = "SELECT {} ({}) FROM {} GROUP BY {} WHERE{} ORDER BY {} ;".format(s_action,", ".join(column), tablename," ".join(result),", ".join(group_field)," ".join(ssa))
        print(query)
    elif isinstance(s_action,list):
        print(x)



    cursor = connection.cursor()
    cursor.execute(query)
    # column_names1 = [column[0] for column in cursor.description]

    # results=cursor.fetchall()
    # csv_value=[] 
    # for row in results:
    #     for value in row:
    #         csv_value.append(value)
    
    
    # def convert_csv(csv_value):
    #     csv_data = [csv_value[i:i+len(column_names1)] for i in range(0, len(csv_value), len(column_names1))]
    #     # print(csv_data)
    #     csv_file_path = 'C:/Users/sakkt/OneDrive/Documents/jana/{}.csv'.format(name)
    #     with open(csv_file_path, 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(column_names1)
    #         writer.writerows(csv_data)
    #         print("CSV file created successfully.")
    # if training_type.lower()=='training':
    #     convert_csv(csv_value)
    
    cursor.close()
    connection.close()
    # return(1)
# except Exception as e:
#     print(e)
#     return(e)    

 

def tp_qp_connector(data1,mod):
    data=data1

    template_version = data[0]['templateVersion']
    type = data[0]['type']
    print(template_version)
    print(type)
    
                        
                    
    if type.lower()=='datasource':
        res=create_table(data)
    elif type.lower()=='insert':
        res=insert_table(data)
    elif type.lower()=='training':
        if 'condition' in data[0]:
            res=training_table1(data)
        elif 'group' in data[0]:
            res=training_table2(data)
    elif type.lower()=='prediction':
        if 'condition' in data[0]:
            res=training_table1(data)
        elif 'group' in data[0]:
            res=training_table2(data)
    print(res)
    return(res)
    
    
            
    
