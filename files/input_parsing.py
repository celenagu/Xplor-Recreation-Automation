import pandas as pd

#constants
file_name = "Service-Drop-Ins.csv"

#reading the file
file = pd.read_csv(file_name)

#getting the names from the specified column
column_name = "Name"          
names = file[column_name].dropna().tolist()  

for current_name in names:
    print(current_name)