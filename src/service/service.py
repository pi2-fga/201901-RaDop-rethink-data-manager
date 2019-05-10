from db.db import (connect, close_connection)
from websockets.exceptions import ConnectionClosed
from concurrent.futures._base import CancelledError
from rethinkdb import RethinkDB
import websockets
import logging
import json
import http
import os


# RethinkDB Global Handler
r = RethinkDB()

# Default localhost address
LOCALHOST = '0.0.0.0'  # nosec

# RethinkDB variables
ReDB_HOST = os.getenv('ReDB_HOST', 'localhost')
ReDB_PORT = os.getenv('ReDB_PORT', 28015)
ReDB_DEFAULT_DB = os.getenv('ReDB_DEFAULT_DB', 'test')
ReDB_USER = os.getenv('ReDB_USER', 'admin')
ReDB_PASS = os.getenv('ReDB_PASS', '')

# WebSocket variables
WS_HOST = os.getenv('WS_HOST', LOCALHOST)
WS_PORT = os.getenv('WS_PORT', 8765)


def health_check(path, request_headers):
    if path == '/health' or path == '/health/':
        logging.info(f'[INFO] HEALTH CHECK PROCESS: {request_headers}')
        return http.HTTPStatus.OK, [], b'Server Up and Running!\n'


def test_database_connection(
        host='localhost',
        port=28015,
        user='admin',
        password=''
        ):
    try:
        connection = connect(host, port, ReDB_DEFAULT_DB, user, password)
        if connection is not None and connection.is_open():
            logging.info(f'[INFO] Connection to database was successful')
        else:
            logging.error(f'[ERROR] Couldn\'t connect to database with:'
                          f'\n HOST: {host}\tPORT: {port}')
            raise Exception('Unknown host and unknown port.')
    except Exception as err:
        logging.error(f'[ERROR] Error at service.py/test_database_connection.'
                      f'\nTraceback: {err}')
        return False
    else:
        if connection is not None and connection.is_open():
            logging.info('[INFO] Closing database connection')
            disconnect_database(connection)

        return True


def configure_database(
        host='localhost',
        port=28015,
        db=None,
        user='admin',
        password=''
        ):
    connection = connect(host, port, db, user, password)
    if db:
        connection.use(db)

    if connection:
        return connection
    else:
        return False


def disconnect_database(connection):
    if not close_connection(connection):
        logging.error(f'[ERROR] Connection with RethinkDB was not closed!')
        return False
    else:
        logging.info(f'[INFO] Connection with RethinkDB was closed'
                     f' successfully!')
        return True


async def changes_listener(websocket, path):
    logging.info(f'[INFO] Current path: {str(path)}')
    try:
        data = await websocket.recv()
        data = json.loads(data)

        try:
            connection = configure_database(
                    ReDB_HOST,
                    ReDB_PORT,
                    ReDB_DEFAULT_DB,
                    ReDB_USER,
                    ReDB_PASS
                )
        except Exception as err:
            if connection:
                disconnect_database(connection)
                raise err
        except KeyboardInterrupt as err:
            disconnect_database(connection)
            raise err
        except ConnectionClosed as err:
            disconnect_database(connection)
            raise err
        except CancelledError as err:
            disconnect_database(connection)
            raise err
        else:
            raise Exception(f'Error at the message received in WebSocket. '
                            f'Couldn\'t decode: {data}')
    except Exception as err:
        logging.error(f'[ERROR] Error at services/changes_listener.'
                      f'\nTraceback: {err}')
    else:
        pass


server = websockets.server.serve(
    changes_listener,
    WS_HOST,
    WS_PORT,
    process_request=health_check,
    ping_timeout=60,
    ping_interval=10
)
