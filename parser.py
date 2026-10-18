def parser(md_full_text):
    lines = md_full_text.readlines()
    if lines[-1].startswith('['):
        
        languages = []
        number_of_languages = int(lines[-1][2]) #максимум 9, может потом улучшить обработку для безлимита

        for i in range(number_of_languages):
            language = lines[-1-i].split(': ')[-1].strip().lower()
            languages.append(language)

        print(languages)