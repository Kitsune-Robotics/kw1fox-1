# Joe wrote this

install:
	sudo cp robotstreamer.service /etc/systemd/system/robotstreamer.service
	sudo systemctl daemon-reload
	sudo systemctl enable robotstreamer.service

test:
	# Runs the tests
	mkdir -p _test
	pipenv run python -m pytest
