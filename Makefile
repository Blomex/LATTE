SHELL := /bin/bash
all:
	( \
	python3 -m venv env; \
	source env/bin/activate; \
	pip install -Iv antlr4-python3-runtime==4.8; \
	)
	cp src/latc_llvm.sh latc_llvm
	chmod u+x latc_llvm
clean:
	rm -rf env
	rm -f latc_llvm
