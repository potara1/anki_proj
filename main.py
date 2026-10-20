from pathlib import Path
import genanki
import zlib

import note_generator
import parser

project_directory = Path(__file__).resolve().parent

notes_directory = project_directory / "Конспекты"
deck_output_directory = project_directory / "Наборы Anki"

for file in notes_directory.glob("*.md"):

    output_anki_file = deck_output_directory / f"{file.stem}.apkg"

    with open(file, 'r') as opened_file:
        parser.parser(opened_file)
    if not translations:
        continue
    
    notes = note_generator.note_generator(translations)

    deck_name = file.stem
    deck_id = zlib.crc32(deck_name.encode())

    deck = genanki.Deck(deck_id, deck_name)

    for note in notes:
        deck.add_note(note)

    genanki.Package(deck).write_to_file(str(output_anki_file))