#import packages
from sqlalchemy import create_engine
import psycopg2
import config
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import os

#connect to postgres database
conn = psycopg2.connect("dbname='*insert dbname*' user=*insert user name* password=*insert passw*")

cur = conn.cursor()

#cur.execute("SELECT model_score FROM stories")
cur.execute("SELECT model_score FROM stories")
records = cur.fetchall()

#remove None values in list
res = []
for val in records:
    if val[0] != None:
        res.append(val[0])
        
# read in your SQL query results using pandas
df1 = pd.read_sql_query("SELECT model_score,model_id, project_id FROM stories",con=conn)
df1.dropna(inplace = True)

       
#import json as pd
df2 = pd.read_json('*insert path to json*')

#records > project id/model id dictionary
#all record pairings uniques 
#output every combination

#zip(df1.model_id, df1.project_id)
#type(zip(df1.model_id, df1.project_id))
#list(zip(df1.model_id, df1.project_id))

df1_id_dict = pd.Series(df1.model_id.values,index=df1.project_id).to_dict()


df2_id_dict = pd.Series(df2.language_model_id.values,index=df2.id).to_dict()

#for loop
for key in df1_id_dict.keys():
    value = df1_id_dict [key]
    df1_proj_mod1 = df1[df1['project_id']==key]
    df1_proj_mod2 = df1_proj_mod1[df1_proj_mod1['model_id']==value]
    
    res2 = df1_proj_mod2['model_score'].values.tolist()


    #add threshold?
    try:
        if df2_id_dict[key]==value:
            Vline='Y'
        else:
            Vline = "N"
    except(KeyError):
        Vline='N' 
            
    if Vline =='Y':
        plt.axvline(x = 0.75, color = 'black', linestyle = '--', label = "threshold")
    else:
        pass
    
    #plot histogram
    plt.hist(res2, bins='auto')
    
    #add title + axis labels

    histogram_title = 'project_id '+str(key)+' + model_id '+str(value)
    plt.title(histogram_title)
    
    plt.xlabel('Model score')
    plt.ylabel('Frequency')
    
    
    #Save and show per plot name
    path= '*insert path to folder*'
    path_name = os.path.join(path, str(histogram_title)+'.png')
    plt.savefig(path_name)
    
    plt.show()
    
conn.close()
