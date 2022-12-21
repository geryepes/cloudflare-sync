
install build reqs:
	apt-get install -y dh-python build-essential devscripts

build deps:
	mk-build-deps -ir

build package:
	dpkg-buildpackage -D