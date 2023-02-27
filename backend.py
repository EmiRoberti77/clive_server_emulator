# %%
import ftplib
import os
import glob
import pandas as pd
import csv
import psycopg2 as ps
from sqlalchemy import create_engine

# %%
HOSTNAME = "mft.next.co.uk"
USERNAME = "video_analysis"
PASSWORD = "Bedf0rd"

# %%
# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# force UTF-8 encoding
ftp_server.encoding = "utf-8"


# %%
path=os.path.abspath(os.getcwd())

# %%
pathdir="txt"
path_dir=os.path.join(path,pathdir)

# %%
try:
    os.mkdir(path_dir)
except OSError as error:
    print(error)

# %%
os.chdir(path_dir)

# %%
for name in ftp_server.nlst("*.txt"):
    with open(name, "wb") as file:
        ftp_server.retrbinary(f"RETR {name}", file.write)

# %%
pathdir="csv"
path_dir_csv=os.path.join(path,pathdir)
try:
    os.mkdir(path_dir_csv)
except OSError as error:
    print(error)

# %%
for filename in glob.glob(os.path.join(path_dir,"*.txt")):
    read_file=pd.read_csv(filename,encoding='unicode_escape')
    changename = filename.replace(path_dir,"").replace(".txt","")
    fl=changename.replace("  ","0")
    fl=fl.replace(" ","")
    read_file.to_csv(path_dir_csv+fl+".csv")

# %%
conn = ps.connect("host=localhost port=5432  dbname=POS user=postgres password=admin")
print("Connecting to Database")

# %%
cur=conn.cursor()

# %%
engine = create_engine('postgresql://postgres:admin@localhost:5432/POS')

# %%
for filename in glob.glob(os.path.join(path_dir_csv,"*.csv")):
    changename=filename.replace(path_dir_csv,"").replace(".csv","")
    df=pd.read_csv(filename)
    fl=changename[1:]
    df.to_sql(fl,con = engine, if_exists= "fail",index=False)

# %%
#ftp_server.quit()


