from pathlib import Path
import genanki
import zlib

import note_generator
import parser
import file_control

project_directory = Path(__file__).resolve().parent

notes_directory = project_directory / "Конспекты"
deck_output_directory = project_directory / "Наборы Anki" # любой локальный путь

all_md_files = []

for file in notes_directory.glob("*.md"):
    
    all_md_files.append(file.name)

    output_anki_file = deck_output_directory / f"{file.stem}.apkg" 

    with open(file, 'r') as opened_file:
        translations = parser.parser(opened_file, file.name)

    if not translations:
        continue

    if file_control.check_for_render_neccessity(file, output_anki_file):
        continue
    
    notes = note_generator.note_generator(translations)

    deck_name = file.stem
    deck_id = zlib.crc32(deck_name.encode())

    deck = genanki.Deck(deck_id, deck_name)

    for note in notes:
        deck.add_note(note)

    genanki.Package(deck).write_to_file(str(output_anki_file))
    file_control.update_exsiting_hash(file)


file_control.check_for_lame_hashes(all_md_files)