from pathlib import Path

import note_generator
import parser

project_directory = Path(__file__).resolve().parent

notes_directory = project_directory / "Конспекты"
deck_output_directory = project_directory / "Наборы Anki"

for file in notes_directory.glob("*.md"):
    with open(file, 'r') as opened_file:
        parser.parser(opened_file)