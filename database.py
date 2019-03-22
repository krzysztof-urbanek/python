import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, insert, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime
import json


Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department = Column(Integer,ForeignKey('department.id'))



db_name = 'KrzysztofUrbanek-1073.postgres.pythonanywhere-services.com:11073/postgres'
#if os.path.exists(db_name):
#    os.remove(db_name)

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://super:poziomka@' + db_name)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
session = Session();

#Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)


for result in session.query(Employee).filter_by(id=1).order_by(Employee.id):
    print(result.id, result.name, result.hired_on,'\n')

session.query(Employee).delete()
session.query(Department).delete()
session.commit()

it = Department()
it.id = 1
it.name = 'IT'

session.add(it)
session.commit()

du = Employee()
du.id = 1
du.name = 'Dariusz Urbanek'
du.hired_on = datetime.date(2018, 12, 15)

session.add(du)

ku = Employee()
ku.id = 2
ku.name = 'Krzysztof Urbanek'
ku.hired_on = datetime.date(2019, 4, 1)
ku.department = 1

session.add(ku)
session.commit()

for instance in session.query(Employee).order_by(Employee.id):
    print(instance.id, instance.name, instance.hired_on)

print('\n')

def tojson(obj,depth):
    if(depth == 0):
        return ''
    try:
        return json.dumps(obj)
    except TypeError:
        try:
            return ','.join([tojson(elem,depth-1) for elem in obj])
        except TypeError:
            return ('<' + str(type(obj)).split('.')[-1].split("'")[0] + ': '
                    + ','.join([str(a) + '=' + tojson(getattr(obj,a),depth-1) for a in dir(obj) if not callable(a) and not str(a).startswith('_') and not str(a) == 'metadata']) + '>')

def totext(obj):
    return [(i, getattr(obj,i)) for i in dir(obj) if not callable(i) and not str(i).startswith('_')]

#for join in session.query(Employee,Department).join(Department):
for join in session.query(Employee,Department).filter((Department.id == Employee.department) | (Employee.id > 1)):
    print(totext(join.Employee),totext(join.Department))



