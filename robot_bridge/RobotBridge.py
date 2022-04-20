# Kitsune Scientific

import argparse
import logging


class RobotBridge:
    def __init__(self, _args) -> None:
        # Copy in args
        self.args = _args

        logging.info(f"Starting RobotBridge, sim mode = {self.args.sim}")

    def run(self):
        while True:
            pass


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
    robotBridge.run()
