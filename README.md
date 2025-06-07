# AutoNest v0.1

AutoNest is a semantic Python code assistant that automatically finds the best place to insert or extend code within an existing project. It supports GPT-based and local semantic analysis, backup versioning, and includes a GUI and CLI interface.

## Features
- Intelligent code insertion & extension
- Backup with versioned sessions
- GUI with semantic color feedback
- GPT-compatible modular structure
- Restore tool with file recovery

See full documentation inside the `/core` and `/interface` directories.

## Requirements
See `requirements.txt`

## Usage
Run the GUI:
```
python interface/autonest_gui.py
```
Run the CLI:
```
python interface/autonest_cli.py
```
Use the restore tool to recover backups:
```
python interface/restore_tool.py
```
After installing with `setup.py`, you can also launch the GUI using the
`autonest-gui` command provided by the console script entry point.
### About the Author

This is my very first Python project. I built AutoNest to learn,
Feedback, ideas, and improvements are welcome!

## Configuration
Edit `config.json` to configure backup location, GPT usage and a default project path.

## Running Tests
Install dev dependencies and run:
```
pytest -v
```

## Continuous Integration
This project uses GitHub Actions to run `black`, `flake8` and the test suite on each push.

