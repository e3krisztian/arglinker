.PHONY: test

all: test clean

test: clean
	python2 test_glued.py
	python3 test_glued.py

clean:
	git clean -df
