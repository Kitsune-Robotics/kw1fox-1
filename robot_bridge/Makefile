# Joe wrote this

install:
	sudo cp robot_bridge.service /etc/systemd/system/robot_bridge.service
	sudo systemctl daemon-reload
	sudo systemctl enable robot_bridge.service

sim:
	pipenv run python RobotBridge.py --sim
