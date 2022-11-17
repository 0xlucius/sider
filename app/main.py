
import asyncio
from .utils import RESPDecoder
from .commands import command_dispatch


def process_command():
    pass


async def response_handler(reader, writer):
    
    while True:
        data = await reader.read(10240)

        if not data:
            break 

        command, *args = RESPDecoder(data).decode()
        command = command.decode()

        writer.write(command_dispatch[command](*args))
        await writer.drain()   

    writer.close()
    await writer.wait_closed()


async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server = await asyncio.start_server(response_handler, "localhost", 6379)
    #server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    #connection, _ = server_socket.accept() # wait for client

    async with server:
        await server.serve_forever()





if __name__ == "__main__":
    asyncio.run(main())
