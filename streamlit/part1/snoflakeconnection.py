import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import snowflake.connector as sc

""" ctx = sc.connect(
 user='SAMANTULAAJAY.KUMAR@LNTINFOTECH.COM',
 password='AjayLti@831',
 account='ona89017',
database = 'MFG_SOL_DB' ,
schema = 'LANDING',
warehouse= 'MFG_SOL_WH',
role = 'SYSADMIN'
)
cs = ctx.cursor()

try:
    cs.execute("select * from KPI_CALCULATION_TEST")
    one_row = cs.fetchone()
    print(one_row)
finally:
    cs.close()
ctx.close() """

url = URL(
    account = 'ona89017',
    user = 'SAMANTULAAJAY.KUMAR@LNTINFOTECH.COM',
    password='AjayLti@831',
    database = 'MFG_SOL_DB' ,
    schema = 'LANDING',
    warehouse= 'MFG_SOL_WH',
    role = 'SYSADMIN'
    #,    authenticator='externalbrowser',
)
engine = create_engine(url)
connection = engine.connect()
query = '''select * from KPI_CALCULATION_TEST'''
data = pd.read_sql(query, connection)
print(data.head())