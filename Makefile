

common:
	echo "Start Installing Common Componenets"
	pip install -r requirements/common.txt
	mkdir log
	
debug: common
	echo "Start Installing Componenets for Debug"
	pip install -r requirements/debug.txt

release: common
	echo "Install Componenets for Release"
	pip install -r requirements/release.txt

test:
	pip install -r requirements/test.txt