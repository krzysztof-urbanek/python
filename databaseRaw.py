import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, insert, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import datetime
import json


metadata = MetaData()


department = Table('department', metadata,
    Column('id',Integer, primary_key=True),
    Column('name',String)
)


employee = Table('employee', metadata,
    Column('id',Integer, primary_key=True),
    Column('name',String),
    Column('hired_on',DateTime, default=func.now()),
    Column('department',Integer,ForeignKey('department.id'))
)


db_name = 'KrzysztofUrbanek-1073.postgres.pythonanywhere-services.com:11073/postgres'

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://super:poziomka@' + db_name)

# metadata.drop_all(engine)

# metadata.create_all(engine)

with engine.connect() as con:
    for row in con.execute(text('select * from employee where id = 1 order by id')):
        print(row.id,row.name,row.hired_on,row.department)


with engine.connect() as con:
    con.execute(text('delete from employee'))

with engine.connect() as con:
    con.execute(text('delete from department'))

with engine.connect() as con:
    con.execute(text('insert into department(id,name) values(:id,:name)'), {'id': 1, 'name': 'IT'})

with engine.connect() as con:
    for row in con.execute(text('select * from department')):
        print(row.id,row.name)

with engine.connect() as con:
    data = (
        {'id': 1, 'name': 'Krzysztof Urbanek', 'hired_on': datetime.date(2019,4,1), 'department': 1},
        {'id': 2, 'name': 'Dariusz Urbanek', 'hired_on': datetime.date(2018,12,15), 'department': None},
    )
    for line in data:
        con.execute(text('insert into employee(id,name,hired_on,department) values(:id,:name,:hired_on,:department)'),line)

with engine.connect() as con:
    for row in con.execute(text('select * from employee')):
        print(row.id,row.name,row.hired_on,row.department)



