from pathlib import Path
import hashlib

file_registry_path = Path(__file__).resolve().parent / 'file_registry.txt'

def init_file_registry():
    if not file_registry_path.exists():
        file_registry_path.touch()

def check_for_render_neccessity(note_path, anki_path):

    skip = False
    detected_files=[]

    init_file_registry()

    with open(file_registry_path, 'a+') as file_registry:

        file_registry.seek(0)
        lines = file_registry.readlines()

        notes_in_registery={}

        with open(note_path, 'r') as note:
            sha_code_of_note = hashlib.sha256(note_path.read_bytes()).hexdigest()

        if lines:
            
            for line in lines:
                note, sha_id = line.strip().split(' --- ')
                notes_in_registery[note]= sha_id

        if note_path.name in notes_in_registery:
            if notes_in_registery[note_path.name] == sha_code_of_note and anki_path.exists():
                skip = True
            

    return skip

def update_exsiting_hash(file):

    notes_in_registry = {}

    with open(file_registry_path, "r", encoding="utf-8") as registry:
        for line in registry:
            if line:
                note, sha = line.strip().split(" --- ")
                notes_in_registry[note] = sha

    notes_in_registry[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()

    with open(file_registry_path, "w", encoding="utf-8") as registry:
        for note, sha in notes_in_registry.items():
            registry.write(f"{note} --- {sha}\n")

def check_for_lame_hashes(all_md_files):

    notes_in_repository = []

    with open(file_registry_path, 'r') as file_registry:
        for line in file_registry.readlines():
            note_in_repository = line.split(' --- ')[0]
            notes_in_repository.append(note_in_repository)

    for note in notes_in_repository:
        if note not in all_md_files:
            print(f'Имеется устаревшая запись о конспекте {note}. Это могло произойти из-за переименовывания файлов. Рекомендуется либо вручную удалить устаревшие записи в реестре, либо сбросить реестр, удалив его')