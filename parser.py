def check_for_safe_footnotes(lines, file_name):
    
    if not lines[-1].strip():
            print(
                f"Конспект {file_name} оканчивается пустой строкой. Это может нарушить определение языков проектом"
            )

def parser(md_full_text, file_name):

    lines = md_full_text.readlines()

    check_for_safe_footnotes(lines, file_name)

    if lines[-1].startswith('['):
        
        languages = {}
        number_of_languages = int(lines[-1][2]) #максимум 9, может потом улучшить обработку для безлимита

        for i in range(number_of_languages):

            language = lines[-1-i].split(': ')[-1].strip().lower()
            language_number = int(lines[-1-i].split(']')[0][2:])
            languages[language_number]=language

        list_of_translations = []
        block = []

    
        for line in lines: #собираем переводы

            line = line.strip()

            if not line: # ищем именно отдельные блоки словаря, другое - уже отдельные блоки
                block = []
                continue

            if line.startswith("* ") and " - " in line:
                word, translation = line[2:].split(" - ", 1)

                language_number = None

                if translation.endswith("]") and "[^" in translation:
                    translation, number = translation.split("[^")
                    language_number = int(number[:-1])

                block.append({
                    "word": word.strip(),
                    "translation": translation.strip(),
                    "language": None
                })

                
                if language_number is not None: # Последнее слово блока со сноской
                    language = languages[language_number]

                    for item in block:
                        item["language"] = language

                    list_of_translations.extend(block)
                    block = []
                    
        return list_of_translations