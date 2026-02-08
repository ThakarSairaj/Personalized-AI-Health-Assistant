#database_con\database.py
# This file is used to connect to the database only

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


url='mysql+pymysql://root:root@localhost:3306/users' # This is the url for the local database connection

engine=create_engine(url, echo=True)

session=sessionmaker(autoflush=False, 
                     autocommit=False, 
                     bind=engine) # This is use to execute the query from the python

base=declarative_base()

