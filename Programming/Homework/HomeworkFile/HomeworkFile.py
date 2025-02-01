result = {}  # {character: [line, line, line]}

with open('roles.txt', 'r', encoding='utf-8') as file_in:
    file_in.readline()
    current_line = file_in.readline().strip()
    while current_line != "textLines:":
        character = current_line
        result[character] = []
        current_line = file_in.readline().strip()

    current_line = file_in.readline()
    line_number = 1
    active_character = ''

    while current_line:
        if current_line[0] != ' ':
            if current_line.strip().split(':', 1)[-1] == '':
                line_number += 1
                active_character = current_line.strip().split(':', 1)[0]
                current_line = file_in.readline()
            else:
                split_line = current_line.strip().split(':', 1)
                character = split_line[0].strip()
                dialogue = split_line[1].strip()
                result[character].append(f'{line_number}) {dialogue}')
                line_number += 1
                active_character = character
                current_line = file_in.readline()
        else:
            dialogue_continuation = current_line.strip()
            if result[active_character] and result[active_character][-1][:len(str(line_number))] == str(line_number):
                result[active_character][-1] += f'    {dialogue_continuation}'
            else:
                result[active_character].append(f'{line_number}) {dialogue_continuation}')
            current_line = file_in.readline()

with open('output.txt', 'w', encoding='utf-8') as file_out:
    file_out.truncate(0)
    for character, dialogues in result.items():
        file_out.write(f'{character}:\n')
        for dialogue in dialogues:
            file_out.write(f'{dialogue}\n')
