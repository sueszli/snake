.PHONY: venv # create virtual environment
venv:
	pip install pip --upgrade
	rm -rf requirements.txt requirements.in .venv
	uvx pipreqs . --mode no-pin --encoding utf-8 --ignore .venv
	mv requirements.txt requirements.in
	uvx --from pip-tools pip-compile requirements.in -o requirements.txt -vvv

	python3.11 -m venv .venv
	./.venv/bin/python3 -m pip install -r requirements.txt
	@echo "activate venv with: \033[1;33msource .venv/bin/activate\033[0m"

.PHONY: lock # freeze dependencies
lock:
	./.venv/bin/python3 -m pip freeze > requirements.in
	uvx --from pip-tools pip-compile requirements.in -o requirements.txt -vvv

.PHONY: fmt # format code
fmt:
	uvx isort .
	uvx autoflake --remove-all-unused-imports --recursive --in-place .
	uvx ruff format --config line-length=5000 .
