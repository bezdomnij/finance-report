import logging
import os
import sys
from dotenv import load_dotenv
import sqlalchemy.sql.sqltypes
from sqlalchemy import create_engine, exc


def write_to_db(df, table_name, db_name='stage', action='replace', hova='19', field_lens=None):
    load_dotenv()
    if hova == '0' or df.empty:
        return
    if field_lens is None:
        field_lens = get_types(df, milyen='mindegy')
    # elif field_lens == 'vchall':
    #     field_lens = get_types(df, milyen='vchall')
    else:
        field_lens = get_types(df, milyen=field_lens)
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
        # username = os.getenv('U_19')
        username = os.getenv('S19_USER')
        pw = os.getenv('S19_PW')
        server = os.getenv('SERVER_1')
    elif which_one == 'pd':
        username = os.getenv('PD_USER')
        pw = os.getenv('PD_PW')
        server = os.getenv('SERVER_2')
    else:
        print("No destination SERVER given! Exiting")
        sys.exit(1)
    # connection_uri = f'mysql+pymysql://{username}:{pw}@{server}:3306/{db_name}?charset=utf8mb4'
    connection_uri = f'mysql+pymysql://{username}:{pw}@{server}:3306/{db_name}?charset=utf8'  # utf8mb4 fucks with joins
    # connect_args = {'init_command': "SET @@collation_connection='utf8mb4_hungarian_ci'", # this causes problems in joining
    #                 'read_timeout': 30}
    connect_args = {'init_command': "SET @@collation_connection='utf8_hungarian_ci'",
                    'read_timeout': 30}
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
                m = get_lengths(df, field)
                lens[field] = 255 if m <= 255 else m
                continue
        typedict = {col_name: sqlalchemy.sql.sqltypes.VARCHAR(length=lens[col_name]) for col_name in lens.keys()}
    elif milyen == 'vchall':
        for col in df.columns:
            if "object" in str(df[col].dtype):
                m = get_lengths(df, col)
                m2 = m if m > 255 else 255
                typedict[col] = sqlalchemy.types.VARCHAR(length=m2)
            else:
                typedict[col] = sqlalchemy.types.VARCHAR(length=255)
    else:
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                m = get_lengths(df, i)
                m2 = m if m > 255 else 255
                typedict.update({i: sqlalchemy.types.VARCHAR(length=m2)})
            if "datetime" in str(j):
                typedict.update({i: sqlalchemy.types.DateTime()})
            if "float" in str(j):
                # typedict.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})
                typedict.update({i: sqlalchemy.types.VARCHAR(length=64)})
            if "int" in str(j):
                # typedict.update({i: sqlalchemy.types.INT()})
                typedict.update({i: sqlalchemy.types.VARCHAR(length=32)})
    return typedict


def get_lengths(df, field):
    df[field] = df[field].astype("str")
    m = max(df[field].str.len())
    return m


if __name__ == '__main__':
    # engine = get_engine('19')
    # engine.dispose()
    print('whatever')
