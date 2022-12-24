import re
import csv
import sqlite3
import pandas as pd
import numpy as np
import string as str
import chardet

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app = Flask(__name__)



app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Documentation for Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers":[],
    "specs":[
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

@swag_from("docs/text.yml", methods=['GET'])
@app.route('/text', methods=['GET'])
def text():
    print ("masuk function")
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': "Halo, apa kabar semua?",
    }
    print ("json_response")
    response_data = jsonify(json_response)
    print(response_data)
    return response_data
    
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])

def text_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', '', text)
    }

    response_data = jsonify(json_response)
    return response_data

   
@swag_from("docs/upload_file.yml", methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload_file():
    upload = request.files.getlist('upload')[0]
    file = upload.read()
    encoding = chardet.detect(file)["encoding"]
    file = file.decode(encoding)
    cleansed_file = re.sub(r'[^a-zA-z0-9]', ' ', file)

    res = {
        'status_code': 200,
        'description': "Cleansed File Result",
        'data': cleansed_file
    }
    datanya = {'sebelumcleansing': [file], 'sesudahcleansing': [cleansed_file]}
    df = pd.DataFrame(datanya)
  
    conn = sqlite3.connect('data/gold.db')
    print("Opened database successfully")
    df.to_sql("data", conn, if_exists='replace')
    
    conn.commit()
    print("Records create successfully")
    conn.close()


    res_json = jsonify(res)
    return res_json


        
if __name__ == '__main__':
    app.debug = True
    app.run()