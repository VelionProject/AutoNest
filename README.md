# AutoNest v0.3

AutoNest is a semantic Python code assistant that automatically finds the best place to insert or extend code within an existing project. It supports GPT-based and local semantic analysis, backup versioning, and includes a GUI and CLI interface.

## Features
- Intelligent code insertion & extension
- Backup with versioned sessions
- GUI with semantic color feedback
- GPT-compatible modular structure
- Restore tool with file recovery
- Plugin system for custom rules
- URL fetching utility via `utils.network_scanner`

See full documentation inside the `/core` and `/interface` directories.

## Requirements
Install the Python packages listed in `requirements.txt` before running AutoNest. Use:
```
pip install -r requirements.txt
```

## Usage
Run the GUI:
```
python -m core.main gui
```
Run the CLI:
```
python -m core.main cli
```
Use the restore tool to recover backups:
```
python -m core.main restore
```
After installing with `setup.py`, you can launch AutoNest using the
`autonest` command provided by the console script entry point.
### About the Author

This is my very first Python project. I built AutoNest to learn,
Feedback, ideas, and improvements are welcome!

## Configuration
Edit `config.json` to configure backup location, GPT usage and a default project path.
You can also set the environment variable `AUTONEST_USE_GPT` ("1" or "0") to
override the `use_gpt` option temporarily.

## Running Tests
Install dev dependencies and run:
```
pytest -v
```

## Continuous Integration
This project uses GitHub Actions to run `black`, `flake8` and the test suite on each push.

