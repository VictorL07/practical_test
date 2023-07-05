import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd
import json, os, re
from sqlalchemy import create_engine

user_db = os.getenv("USER_DB", "vlujanr")
user_pass = os.getenv("USER_PASS", "njfoM5G7ySgr")
db_address = os.getenv("DB_ADRESS", "ep-autumn-wood-396348.us-east-2.aws.neon.tech/neondb")
CONNSTR = f'postgresql://{user_db}:{user_pass}@{db_address}'
UPLOAD_FOLDER = 'static/files'

# Crear un motor de conexión
engine = create_engine(CONNSTR)

def sql_ingest_api(file_path):
    # Load config file
    with open("/app/src/config.json") as json_file:
        jsonobject = json.load(json_file)

    # set table name
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    for key in jsonobject:
            match = re.search(key["key_table"], table_name)
            if match:
                col_names = key["columns"].split(",") 
                # read file 
                df = pd.read_csv(file_path, header=None, names=col_names)
                # upload table in db
                df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
                # get records upload
                with engine.connect() as connection:
                    count = pd.read_sql_query(f'SELECT COUNT(*) FROM {table_name}', connection).iloc[0,0]
                result = json.dumps({'table': table_name ,'insert_rows': str(count)})
                return result
            
def number_employee_by_year(year):
    query = f"""
        SELECT he.id, job, department, datetime as hired_date, date_part('quarter',date(datetime)) as quarter
        FROM hired_employees as he
        LEFT JOIN departments as d ON he.department_id = d.id
        LEFT JOIN jobs as j ON he.job_id = j.id
        WHERE date_part('year',date(datetime)) = '{year}'
     """
    # Carga la consulta en un DataFrame
    df_year = pd.read_sql_query(query, engine)
    df_year['quarter'] = df_year['quarter'].apply(lambda x: f"Q{int(x)}")

    # Agrupa los datos por trimestre, departamento y trabajo, y cuenta el número de empleados en cada grupo
    result = df_year.groupby(['quarter', 'department', 'job']).size().reset_index()

    pivot_df = result.pivot(index=['department', 'job'], columns='quarter', values=0)
    pivot_df = pivot_df.fillna(0)
    pivot_df = pivot_df.reset_index()
    json_data = pivot_df.to_json(orient='table',index=False)

    return json_data

def employee_list_by_department(year):
    query = f"""
        SELECT he.id as employee_id, d.id, department, datetime as hired_date
        FROM hired_employees as he
        LEFT JOIN departments as d ON he.department_id = d.id
        LEFT JOIN jobs as j ON he.job_id = j.id
        WHERE date_part('year',date(datetime)) = '{year}'
    """
    df_year = pd.read_sql_query(query, engine)

    # Calculamos el número de empleados contratados por departamento
    dept_hires = df_year[['id','department']].value_counts().reset_index()
    dept_hires.columns = ['id','department', 'num_hires']
    # Calculamos la media de empleados contratados en 2021
    mean_hires = dept_hires['num_hires'].mean()
    # Filtramos los departamentos que contrataron más empleados que la media
    top_depts = dept_hires[dept_hires['num_hires'] > mean_hires]
    # Ordenamos por el número de contrataciones (descendente)
    top_depts = top_depts.sort_values('num_hires', ascending=False)
    json_data = top_depts.to_json(orient='table',index=False)
    return json_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Routes
@app.route('/', methods=['POST'])
def uploadFiles():
    try:
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            data_ingest = sql_ingest_api(file_path)
            # save the file
            return data_ingest, 201
        else:
            return {"message":"This is not a file"}, 500
    except Exception as e:
        return {"message":f"{e}"}, 500

@app.route('/api/employee/number_by_year', methods=['POST'])
def number_by_year():
    try:
        data = request.get_json()
        year = data["year"]
        if isinstance(year, str):
            result_nby = number_employee_by_year(year)
            return result_nby, 201
        else:
            return {"message":"This value isnt a string"}, 500
    except Exception as e:
        return {"message":f"{e}"}, 500

@app.route('/api/employee/list_by_deparment', methods=['POST'])
def list_by_deparment():
    try:
        data = request.get_json()
        year = data["year"]
        if isinstance(year, str):
            result_lbd = employee_list_by_department(year)
            return result_lbd, 201
        else:
            return {"message":"This value isnt a string"}, 500
    except Exception as e:
        return {"message":f"{e}"}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)