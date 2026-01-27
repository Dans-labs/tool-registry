export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
PORT ?= 8000

.PHONY: run sync force-sync
run: sync
	uvicorn src.main:app --host 0.0.0.0 --port $(PORT) --reload

sync:
	uv sync 

force-sync:
	rm uv.lock
	uv sync --force-reinstall

