import genanki

def note_generator(list_of_translations):
    
    notes = []

    for item in list_of_translations:
        note = genanki.Note(
            model=genanki.BASIC_MODEL,
            fields=[item['word'], item['translation']]
        )

        notes.append(note)

    return notes

