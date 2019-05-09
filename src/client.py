import asyncio
import websockets
import json
from websockets import ConnectionClosed


async def hello():
    async with websockets.connect(
            'ws://10.30.0.94:8765/status') as websocket:
        name = input("Paycheck ID: ")
        data = {'paycheck_identifier': name}

        await websocket.send(json.dumps(data))
        print(f"> {name}")

        try:
            while True:
                await websocket.pong(data='PONG')
                message = await asyncio.wait_for(websocket.recv(), timeout=20)
                print(f"< {message}")
                if message is None:
                    break
        except (asyncio.TimeoutError, ConnectionRefusedError) as err:
            print(err)
        except ConnectionClosed as err:
            print(err)
        except RuntimeError as err:
            print(err)
        except Exception as err:
            print(err)
        finally:
            asyncio.get_event_loop().stop()


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello())
except (asyncio.TimeoutError, ConnectionRefusedError) as err:
    print(err)
except ConnectionClosed as err:
    print(err)
except RuntimeError as err:
    print(err)
except Exception as err:
    print(err)
finally:
    asyncio.get_event_loop().stop()
