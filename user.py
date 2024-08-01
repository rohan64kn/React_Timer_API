from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import meta
from schema_index import Credentials, Machine_Uptimes, Machine_Offtimes, User_Logs
credentials = Table(
'Credentials', meta,
Column('username',String(255), primary_key=True),
Column('password',Integer))
machine_uptime=Table('Machine_Uptimes',meta,
Column('machineontime',Integer))
mahine_offtime=Table(
'Machine_Offtimes',meta,
Column('machineofftime',Integer))
user_logs=Table(
'User_Logs',meta,
Column('username',String(255), primary_key=True),
Column('logintime',Integer)
)