# Kitsune Scientific

import socket
import asyncio
import logging
import argparse


class RobotBridge:
    def __init__(self, _args) -> None:
        # Copy in args
        self.args = _args

        # Socket/Server
        self.host = "localhost"
        self.port = 15555

        logging.info(f"Starting RobotBridge, sim mode = {self.args.sim}")

    async def handle_client(self, reader, writer):
        request = None

        while request != "quit":
            request = (await reader.read(255)).decode("utf8")

            response = str(request)

            writer.write(response.encode("utf8"))

            logging.info(f'Got a new instruction "{response}"')

            await writer.drain()

        writer.close()
        logging.warning("Client disconnected from session!")

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.DEBUG)

    # Argument parser
    parser = argparse.ArgumentParser(description="Robot Bridge Args.")
    parser.add_argument("--sim", default=False, action="store_true")

    # Parse args
    args = parser.parse_args()

    # Make a bridge
    robotBridge = RobotBridge(args)

    # Run the bridge
    asyncio.run(robotBridge.run())
