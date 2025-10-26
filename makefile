.PHONY: venv # create virtual environment
venv:
	uv venv
	uv pip install -r requirements.in
	@echo "activate venv with: \033[1;33msource .venv/bin/activate\033[0m"

.PHONY: lock # freeze dependencies
lock:
	uv pip freeze > requirements.txt

.PHONY: fmt # format code
fmt:
	uvx isort .
	uvx autoflake --remove-all-unused-imports --recursive --in-place .
	uvx ruff format --config line-length=5000 .
