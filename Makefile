# Variables
VENV := venv
OS := $(shell uname 2>/dev/null || echo Windows)

# Detect correct Python and Pip commands for venv
ifeq ($(OS), Windows)
	PYTHON := $(VENV)/Scripts/python.exe
	PIP := $(VENV)/Scripts/pip.exe
	CLEAR_CMD := cls
	TIME_CMD :=
else
	PYTHON := $(VENV)/bin/python3
	PIP := $(VENV)/bin/pip
	CLEAR_CMD := clear
	TIME_CMD := time
endif

# Main target that runs the scripts
all: run

# Main Scripts:
run: $(VENV)
	$(CLEAR_CMD)
	$(TIME_CMD) $(PYTHON) ./table_generator.py

# Setup Virtual Environment and Install Dependencies
$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Install the project dependencies
dependencies: $(VENV)

# Generate requirements.txt from the current venv
generate_requirements: $(VENV)
	$(PIP) freeze > requirements.txt

# Utility rule for cleaning the project
clean:
	rm -rf $(VENV) || rmdir /S /Q $(VENV) 2>nul
	find . -type f -name '*.pyc' -delete || del /S /Q *.pyc 2>nul
	find . -type d -name '__pycache__' -delete || rmdir /S /Q __pycache__ 2>nul

.PHONY: all run clean dependencies generate_requirements
