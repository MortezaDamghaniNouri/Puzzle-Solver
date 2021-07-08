
class node:
    def __init__(self, identifier):
        self.id = identifier
        self.parent_id = ""
        self.domain = []







# This function checks if the input character is a number or not
def is_number(input_char):
    if input_char == "0" or input_char == "1" or input_char == "2" or input_char == "3" or input_char == "4" or input_char == "5" or input_char == "6" or input_char == "7" or input_char == "8" or input_char == "9":
        return True
    else:
        return False


# This function reads the input file
def file_reader():
    file_name = input("Enter the full name of the input file(it must contain .txt): ")
    input_file = open("puzzles/" + file_name, "rt")
    chunk = input_file.read(1)
    number_of_rows = ""
    while is_number(chunk):
        number_of_rows += chunk
        chunk = input_file.read(1)
    number_of_rows = int(number_of_rows)
    while chunk != '\n':
        chunk = input_file.read(1)
    input_matrix = []
    while chunk:
        temp = []
        counter = 1
        while counter <= number_of_rows:
            chunk = input_file.read(1)
            temp.append(chunk)
            chunk = input_file.read(1)
            counter += 1
        input_matrix.append(temp)
    return input_matrix, number_of_rows


# This function generates the nodes which are the variables without any assigned value
def nodes_generator(input_matrix, input_number_of_rows):
    nodes = []
    i = 0
    while i < input_number_of_rows:
        j = 0
        while j < input_number_of_rows:
            if input_matrix[i][j] == '-':
                key = str(i) + "," + str(j)
                temp_object = node(key)
                temp_object.domain.append("0")
                temp_object.domain.append("1")
                nodes.append(temp_object)
            j += 1
        i += 1
    return nodes


# This function separates the row part and the column part of an input string
def row_and_column_finder(input_string):
    index = input_string.find(',')
    input_list = list(input_string)
    row = ""
    column = ""
    i = 0
    while i < index:
        row += input_list[i]
        i += 1
    i += 1
    while i < len(input_list):
        column += input_list[i]
        i += 1

    return int(row), int(column)


# This function finds all of the strings in rows and columns
def all_strings_finder(input_matrix, number_of_rows):
    strings = []
    i = 0
    while i < number_of_rows:
        all_assigned = True
        j = 0
        temp = ""
        while j < number_of_rows:
            if input_matrix[i][j] == "-":
                all_assigned = False
                break
            else:
                temp += input_matrix[i][j]
            j += 1
        if all_assigned:
            strings.append(temp)
        i += 1

    i = 0
    while i < number_of_rows:
        all_assigned = True
        j = 0
        temp = ""
        while j < number_of_rows:
            if input_matrix[j][i] == "-":
                all_assigned = False
                break
            else:
                temp += input_matrix[j][i]
            j += 1
        if all_assigned:
            strings.append(temp)
        i += 1

    return strings






# Forward checking part of the algorithm is implemented here
def forward_checker(input_matrix, nodes, number_of_rows):
    # The equal number of zeros and ones in each row and column is implemented here
    for node in nodes:
        row, column = row_and_column_finder(node.id)
        # Checking if the number of zeros and ones are equal in a row
        just_one_remain_in_row = True
        j = 0
        while j < number_of_rows:
            if j != column:
                if input_matrix[row][j] == "-":
                    just_one_remain_in_row = False
                    break
            j += 1

        if just_one_remain_in_row:
            one_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[row][j] == "1":
                    one_counter += 1
                j += 1
            zero_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[row][j] == "0":
                    zero_counter += 1
                j += 1


            if zero_counter > one_counter:
                node.domain.remove("0")
            if one_counter > zero_counter:
                node.domain.remove("1")

        just_one_remain_in_column = True
        j = 0
        while j < number_of_rows:
            if j != row:
                if input_matrix[j][column] == "-":
                    just_one_remain_in_column = False
                    break
            j += 1
        if just_one_remain_in_column:
            one_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[j][column] == "1":
                    one_counter += 1
                j += 1
            zero_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[j][column] == "0":
                    zero_counter += 1
                j += 1
            if zero_counter > one_counter:
                node.domain.remove("0")
            if one_counter > zero_counter:
                node.domain.remove("1")

        # Checking different strings in columns and rows constraint
        strings = all_strings_finder(input_matrix, number_of_rows)








# Main part of the code starts here
input_matrix, number_of_rows = file_reader()
print(input_matrix)

nodes = nodes_generator(input_matrix, number_of_rows)


forward_checker(input_matrix, nodes, number_of_rows)



























