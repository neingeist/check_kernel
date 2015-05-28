.PHONY: default install

default:
	echo "Use 'make install' to install"

install:
	install -oroot -groot check_kernel /usr/lib/nagios/plugins/
