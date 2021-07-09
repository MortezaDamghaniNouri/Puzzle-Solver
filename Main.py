import random


class node:
    def __init__(self, identifier):
        self.id = identifier
        self.parent = ""
        self.domain = []
        # If this variable is true, it means that the node is assigned a value
        self.assigned = False
        self.value = ""







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


# This function finds all of the strings in rows
def row_strings_finder(input_matrix, number_of_rows):
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
    return strings


# This function finds all of the strings in rows
def column_strings_finder(input_matrix, number_of_rows):
    strings = []
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
        if not node.assigned:
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
                    if "0" in node.domain:
                        node.domain.remove("0")
                if one_counter > zero_counter:
                    if "1" in node.domain:
                        node.domain.remove("1")

                # Checking different strings in columns and rows constraint
                row_strings = row_strings_finder(input_matrix, number_of_rows)
                if len(row_strings) > 0:
                    current_row_string = ""
                    j = 0
                    while j < number_of_rows:
                        current_row_string += input_matrix[row][j]
                        j += 1
                    dash_index = current_row_string.find("-")
                    current_row_list = list(current_row_string)
                    if "0" in node.domain:
                        current_row_list[dash_index] = "0"
                        current_row_string = str(current_row_list)
                        if current_row_string in row_strings:
                            node.domain.remove("0")
                    if "1" in node.domain:
                        current_row_list[dash_index] = "1"
                        current_row_string = str(current_row_list)
                        if current_row_string in row_strings:
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
                    if "0" in node.domain:
                        node.domain.remove("0")
                if one_counter > zero_counter:
                    if "1" in node.domain:
                        node.domain.remove("1")

                # Checking different strings in columns and rows constraint
                column_strings = column_strings_finder(input_matrix, number_of_rows)
                if len(column_strings) > 0:
                    current_column_string = ""
                    j = 0
                    while j < number_of_rows:
                        current_column_string += input_matrix[j][column]
                        j += 1
                    dash_index = current_column_string.find("-")
                    current_column_list = list(current_column_string)
                    if "0" in node.domain:
                        current_column_list[dash_index] = "0"
                        current_column_string = str(current_column_list)
                        if current_column_string in column_strings:
                            node.domain.remove("0")
                    if "1" in node.domain:
                        current_column_list[dash_index] = "1"
                        current_column_string = str(current_column_list)
                        if current_column_string in column_strings:
                            node.domain.remove("1")

            # Checking not more than row equal numbers in a column constraint
            if row - 1 >= 0 and row + 1 < number_of_rows and input_matrix[row - 1][column] == input_matrix[row + 1][
                column] and input_matrix[row - 1][column] != "-":
                value = input_matrix[row - 1][column]
                if value in node.domain:
                    node.domain.remove(value)
            if row - 2 >= 0 and input_matrix[row - 2][column] == input_matrix[row - 1][column] and \
                    input_matrix[row - 2][column] != "-":
                value = input_matrix[row - 2][column]
                if value in node.domain:
                    node.domain.remove(value)
            if row + 2 < number_of_rows and input_matrix[row + 2][column] == input_matrix[row + 1][column] and \
                    input_matrix[row + 2][column] != "-":
                value = input_matrix[row + 2][column]
                if value in node.domain:
                    node.domain.remove(value)

            # Checking not more than row equal numbers in a row constraint
            if column - 1 >= 0 and column + 1 < number_of_rows and input_matrix[row][column - 1] == input_matrix[row][
                column + 1] and input_matrix[row][column - 1] != "-":
                value = input_matrix[row][column - 1]
                if value in node.domain:
                    node.domain.remove(value)
            if column - 2 >= 0 and input_matrix[row][column - 2] == input_matrix[row][column - 1] and input_matrix[row][column - 2] != "-":
                value = input_matrix[row][column - 2]
                if value in node.domain:
                    node.domain.remove(value)
            if column + 2 < number_of_rows and input_matrix[row][column + 2] == input_matrix[row][column + 1] and input_matrix[row][column + 2] != "-":
                value = input_matrix[row][column + 2]
                if value in node.domain:
                    node.domain.remove(value)


# This function selects a node by MRV method
def minimum_remaining_value_finder(nodes):
    i = 0
    minimum_remaining_node = ""
    while i < len(nodes):
        if not nodes[i].assigned:
            minimum_remaining_node = nodes[i]
            break
        i += 1
    if minimum_remaining_node != "":
        for node in nodes:
            if not node.assigned:
                if len(node.domain) < len(minimum_remaining_node.domain):
                    minimum_remaining_node = node
    return minimum_remaining_node


# This function assigns a value to the input node
def random_assigner(node):
    if len(node.domain) == 1:
        node.value = node.domain[0]
    else:
        random_index = random.randint(0, 1)
        node.value = node.domain[random_index]


# This function generates a copy of the input matrix
def matrix_copier(input_matrix):
    copy_matrix = []
    for k in input_matrix:
        temp = []
        for m in k:
            temp.append(m)
        copy_matrix.append(temp)
    return copy_matrix


# This function checks if repetition exists among strings in the input list
def does_repetition_exist(input_list):
    i = 0
    while i < len(input_list) - 1:
        j = i + 1
        while j < len(input_list):
            if input_list[i] == input_list[j]:
                return True
            j += 1
        i += 1
    return False











# Main part of the code starts here
input_matrix, number_of_rows = file_reader()
# print(input_matrix)
input_matrix_copy = matrix_copier(input_matrix)
nodes = nodes_generator(input_matrix, number_of_rows)
forward_checker(input_matrix, nodes, number_of_rows)
root = minimum_remaining_value_finder(nodes)
random_assigner(root)
row, column = row_and_column_finder(root.id)
input_matrix[row][column] = root.value
root.assigned = True
root.parent = node("1")   # This is the root's parent id for finding it
root.domain.remove(root.value)
number_of_assigned_nodes = 1
previous_selected_node = root
error_counter = 0
current_node = minimum_remaining_value_finder(nodes)
current_node.parent = root
error = False
# Backtracking algorithm is implemented here
while number_of_assigned_nodes != len(nodes):
    if len(current_node.domain) == 0:
        if current_node.parent != "" and current_node.parent.id == "1":
            error_counter += 1
            if error_counter == 10:
                print("Error")
                error = True
                break
            else:
                input_matrix = input_matrix_copy
                input_matrix_copy = matrix_copier(input_matrix)
                nodes = nodes_generator(input_matrix, number_of_rows)
                forward_checker(input_matrix, nodes, number_of_rows)
                root = minimum_remaining_value_finder(nodes)
                random_assigner(root)
                row, column = row_and_column_finder(root.id)
                input_matrix[row][column] = root.value
                root.assigned = True
                root.parent = node("1")
                root.domain.remove(root.value)
                number_of_assigned_nodes = 1
                previous_selected_node = root
                current_node = minimum_remaining_value_finder(nodes)
                current_node.parent = root
        else:
            current_node.domain.append("0")
            current_node.domain.append("1")
            current_node.value = ""
            current_node.assigned = False
            row, column = row_and_column_finder(current_node.id)
            input_matrix[row][column] = "-"
            if current_node.parent != "":
                temp = current_node
                current_node = current_node.parent
                previous_selected_node = current_node.parent
                temp.parent = ""
                number_of_assigned_nodes = number_of_assigned_nodes - 1
            else:
                temp = current_node
                current_node = previous_selected_node
                previous_selected_node = current_node.parent
                temp.parent = ""
                number_of_assigned_nodes = number_of_assigned_nodes - 1

    else:
        random_assigner(current_node)
        row, column = row_and_column_finder(current_node.id)
        input_matrix[row][column] = current_node.value
        current_node.assigned = True
        number_of_assigned_nodes += 1
        current_node.domain.remove(current_node.value)
        current_node.parent = previous_selected_node
        previous_selected_node = current_node
        current_node = minimum_remaining_value_finder(nodes)
        if number_of_assigned_nodes != len(nodes):
            forward_checker(input_matrix, nodes, number_of_rows)
        else:
            row_strings = row_strings_finder(input_matrix, number_of_rows)
            column_strings = column_strings_finder(input_matrix, number_of_rows)
            if does_repetition_exist(row_strings) or does_repetition_exist(column_strings):
                input_matrix = input_matrix_copy
                input_matrix_copy = matrix_copier(input_matrix)
                nodes = nodes_generator(input_matrix, number_of_rows)
                forward_checker(input_matrix, nodes, number_of_rows)
                root = minimum_remaining_value_finder(nodes)
                random_assigner(root)
                row, column = row_and_column_finder(root.id)
                input_matrix[row][column] = root.value
                root.assigned = True
                root.parent = node("1")
                root.domain.remove(root.value)
                number_of_assigned_nodes = 1
                previous_selected_node = root
                error_counter = 0
                current_node = minimum_remaining_value_finder(nodes)
                current_node.parent = root
                error = False





if not error:
    for i in input_matrix:
        line = ""
        for j in i:
            line += j + "    "
        print(line)




















































