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
        """
        A handle_client is spawned per client
        """
        request = None

        while request != "quit":
            # Decode request
            request = str((await reader.read(255)).decode("utf8"))
            logging.debug(f'Got a new instruction "{request}"')

            # Construct response
            response = request
            writer.write(response.encode("utf8"))  # Send response
            logging.debug(f'Sent reply to instruction "{request}", "{response}"')

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
