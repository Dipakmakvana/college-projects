"""A small, persistent command-line manager for school subjects."""

import json
import os
import tempfile
from pathlib import Path
from typing import List


DATA_FILE = Path(__file__).with_name("subjects.json")
MAX_SUBJECT_LENGTH = 80


def load_subjects(data_file: Path = DATA_FILE) -> List[str]:
    """Load saved subjects, returning an empty list when no data exists yet."""
    if not data_file.exists():
        return []

    try:
        saved_value = json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            "The saved subjects file is not valid JSON. "
            "Repair or move subjects.json before starting the program again."
        ) from error

    if not isinstance(saved_value, list) or any(
        not isinstance(subject, str) for subject in saved_value
    ):
        raise ValueError(
            "The saved subjects file must contain a JSON list of subject names."
        )

    subjects = []
    seen_subjects = set()
    for subject in saved_value:
        cleaned_subject = subject.strip()
        normalized_subject = cleaned_subject.casefold()
        if cleaned_subject and normalized_subject not in seen_subjects:
            subjects.append(cleaned_subject)
            seen_subjects.add(normalized_subject)

    return subjects


def save_subjects(subjects: List[str], data_file: Path = DATA_FILE) -> None:
    """Save subjects safely by replacing the data file after writing a temp file."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(data_file.parent),
            prefix=".subjects-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(subjects, temporary_file, ensure_ascii=False, indent=2)
            temporary_file.write("\n")
            temporary_path = temporary_file.name

        os.replace(temporary_path, str(data_file))
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


def add_subject(subjects: List[str], data_file: Path = DATA_FILE) -> None:
    subject = input("Enter a subject name: ").strip()

    if not subject:
        print("Subject name cannot be empty.\n")
        return

    if len(subject) > MAX_SUBJECT_LENGTH:
        print(
            "Subject name must be "
            f"{MAX_SUBJECT_LENGTH} characters or fewer.\n"
        )
        return

    if any(existing.casefold() == subject.casefold() for existing in subjects):
        print("That subject is already in the list.\n")
        return

    subjects.append(subject)
    try:
        save_subjects(subjects, data_file)
    except OSError as error:
        subjects.pop()
        print(f"Could not save the subject: {error}\n")
        return

    print(f"Added '{subject}'.\n")


def remove_subject(subjects: List[str], data_file: Path = DATA_FILE) -> None:
    subject = input("Enter the subject name to remove: ").strip()

    if not subject:
        print("Subject name cannot be empty.\n")
        return

    for index, existing in enumerate(subjects):
        if existing.casefold() == subject.casefold():
            removed_subject = subjects.pop(index)
            try:
                save_subjects(subjects, data_file)
            except OSError as error:
                subjects.insert(index, removed_subject)
                print(f"Could not save the change: {error}\n")
                return

            print(f"Removed '{removed_subject}'.\n")
            return

    print("Subject not found.\n")


def display_subjects(subjects: List[str]) -> None:
    if not subjects:
        print("No subjects have been added yet.\n")
        return

    print("\nYour subjects:")
    for index, subject in enumerate(subjects, start=1):
        print(f"{index}. {subject}")
    print(f"Total: {len(subjects)} subject(s).\n")


def main(data_file: Path = DATA_FILE) -> None:
    try:
        subjects = load_subjects(data_file)
    except (OSError, ValueError) as error:
        print(f"Could not load saved subjects: {error}")
        return

    print("====== SCHOOL SUBJECTS MANAGER ======")

    while True:
        print("1) Add a subject")
        print("2) Remove a subject")
        print("3) Display subjects")
        print("4) Exit")

        choice = input("Choose an option (1-4): ").strip()
        print()

        if choice == "1":
            add_subject(subjects, data_file)
        elif choice == "2":
            remove_subject(subjects, data_file)
        elif choice == "3":
            display_subjects(subjects)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")

