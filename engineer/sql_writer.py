import logging
import os
import sys

import sqlalchemy.sql.sqltypes
from sqlalchemy import create_engine, exc


def write_to_db(df, table_name, db_name='stage', action='replace', hova='19', field_lens=None):
    if field_lens is None:
        field_lens = get_types(df, milyen='mindegy')
    try:
        sql_engine = get_engine(hova, db_name=db_name)
        connection = sql_engine.connect()
    except exc.OperationalError as e:
        logging.exception(msg=f'logged error SQL write: {e}')
        print(f'fuck, SQL credentials need improvement. Error: {e}')
        return
    try:
        df.to_sql(table_name, connection, if_exists=action, index=False,
                  method='multi', chunksize=5000, dtype=field_lens)
    except Exception as e:
        logging.exception(e)
        print(f'BIG RED FLAG, this is, {e.__str__}: check the logfile for details!!!{table_name}')
    else:
        print(f"Table {table_name} is written to successfully.")
    finally:
        try:
            connection.close()
            # engine.dispose()
        except AttributeError as e:
            print(f'Nothing to close, no connection. Error: {e}')


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
    # connect_args = {'init_command': "SET @@collation_connection='utf8_hungarian_ci'",
    #                 'read_timeout': 30}
    try:
        sql_engine = create_engine(connection_uri, pool_pre_ping=True, pool_recycle=3600, echo=False,
                                   echo_pool=False, connect_args=connect_args, future=False)
    except Exception as e:
        print(f'NO connection, error: {e}')
        return
    return sql_engine


def get_types(df, milyen='mindegy'):
    typedict = {}
    lens = {}
    if milyen == 'mindegy' and len(df) > 0:
        for field in df.columns:
            try:
                max_length = len(max(df[field], key=len))
                if max_length > 255:
                    print("Long field! ", max_length, field)
                    lens[field] = max_length
                else:
                    lens[field] = 255
            except Exception as e:
                logging.exception(msg=f'LOGERROR: {e} in field: ||| {field}')
                df[field] = df[field].astype("str")
                m = max(df[field].str.len())
                lens[field] = 255 if m < 255 else m
                continue
        typedict = {col_name: sqlalchemy.sql.sqltypes.VARCHAR(length=lens[col_name]) for col_name in lens.keys()}
    else:
        for i, j in zip(df.columns, df.dtypes):
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
    # engine = get_engine('19')
    # engine.dispose()
    print('whatever')
