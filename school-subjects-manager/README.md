# School Subjects Manager

A small Python command-line app for keeping a subject list. It saves the list as JSON beside the program, so subjects are still there the next time it runs.

## Features

- Add and remove subjects
- Display the current list and its total
- Reject blank names and duplicate names, ignoring capitalization
- Save changes to `subjects.json`
- Keep the previous saved file if a save is interrupted
- Use only the Python standard library

## Requirements

- Python 3.8 or newer

## Run

Open a terminal in this folder and run:

```powershell
python school_subjects_manager.py
```

The program creates `subjects.json` on the first successful change. Keep the script in a folder where your account can create and update files.

## Project structure

```text
school-subjects-manager/
├── README.md
└── school_subjects_manager.py
```

## How it works

The program loads the JSON list at startup, validates each menu choice, and saves changes through a temporary file before replacing the previous data file. Subject comparisons use `casefold()`, so `Math` and `math` count as the same subject.

## Ideas for a next version

- Store a subject code, semester, and teacher for each subject
- Move from JSON to SQLite
- Add a Flask web interface

