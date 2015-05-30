.PHONY: test

all: test clean

test: clean
	python2 test_arglinker.py
	python3 test_arglinker.py

clean:
	git clean -df
