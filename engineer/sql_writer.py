import os
import sys

import sqlalchemy.sql.sqltypes
from sqlalchemy import create_engine


def write_to_db(df, table_name, action='replace', hova='19'):
    try:
        sql_engine = get_engine(hova, db_name='stage')
        connection = sql_engine.connect()
    except Exception as e:
        print(f'SQL credentials need improvement. Error: {e}')
        return

    types = get_types(df, milyen='mindegy')
    try:
        df.to_sql(table_name, connection, if_exists=action, index=False,
                  method='multi', chunksize=20000, dtype=types)
    except ValueError as vx:
        print('ERROR!!! df not created : ', vx)
    else:
        print(f"Table {table_name} is written to successfully.")
    finally:
        connection.close()


def get_engine(which_one, db_name='stage'):
    if which_one == '19':
        username = os.getenv('U_19')
        pw = os.getenv('P_19')
        server = '192.168.2.19'
    elif which_one == 'pd':
        username = os.getenv('U_PD')
        pw = os.getenv('P_PD')
        server = '10.123.4.13'
    else:
        print("No destination SERVER given! Exiting")
        sys.exit(1)
    connection_uri = f'mysql+pymysql://{username}:{pw}@{server}:3306/{db_name}?charset=utf8mb4'
    connect_args = {'init_command': "SET @@collation_connection='utf8mb4_hungarian_ci'",
                    'read_timeout': 30}
    try:
        sql_engine = create_engine(connection_uri, pool_pre_ping=True, pool_recycle=3600, echo=False,
                                   echo_pool=True, connect_args=connect_args, future=False)
    except Exception as e:
        print(f'NO connection, error: {e}')
        return
    return sql_engine


def get_types(dfparam, milyen='mindegy'):
    typedict = {}
    if milyen == 'mindegy':
        typedict = {col_name: sqlalchemy.sql.sqltypes.VARCHAR(length=255) for col_name in dfparam}
    else:
        for i, j in zip(dfparam.columns, dfparam.dtypes):
            if "object" in str(j):
                typedict.update({i: sqlalchemy.types.NVARCHAR(length=255)})
            if "datetime" in str(j):
                typedict.update({i: sqlalchemy.types.DateTime()})
            if "float" in str(j):
                typedict.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})
            if "int" in str(j):
                typedict.update({i: sqlalchemy.types.INT()})
    return typedict


if __name__ == '__main__':
    engine = get_engine('19')
    engine.dispose()
    print('whatever')
