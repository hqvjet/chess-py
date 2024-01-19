def get_board_from_file(filename):
    result_string = ''
    filename = "res/" + filename
    # Read the file and process each line
    with open(filename, 'r') as file:
        for line in file:
            result_string += line.strip() + '\n'

    return result_string

print(get_board_from_file('board_temp.txt'))
