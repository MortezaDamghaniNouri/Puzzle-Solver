# This library is used for generating random numbers for randomly choosing among some variables and values
import random
# This library is imported for time measurement
import time


# This class specifies each node in backtracking algorithm
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
    while True:
        algorithm_number = input("Enter the number of algorithm you want to run: \n1)Forward Checking\n2)MAC(Maintaining Arc Consistency)\n")
        if algorithm_number == "1" or algorithm_number == "2":
            break
        print("Wrong input")
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
    return input_matrix, number_of_rows, algorithm_number


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


# This function checks the equal number of ones and zeros in a row and a column
def equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows):
    i = 0
    while i < number_of_rows:
        dash_counter = 0
        dashed_cells = []
        j = 0
        while j < number_of_rows:
            if input_matrix[i][j] == "-":
                dash_counter += 1
                dashed_cells.append(str(i) + "," + str(j))
            j += 1
        if dash_counter == 1:
            k = 0
            while k < len(nodes):
                if nodes[k].id == dashed_cells[0]:
                    dashed_node = nodes[k]
                    break
                k += 1
            one_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[i][j] == "1":
                    one_counter += 1
                j += 1
            zero_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[i][j] == "0":
                    zero_counter += 1
                j += 1
            if zero_counter > one_counter:
                if "0" in dashed_node.domain:
                    dashed_node.domain.remove("0")
            if one_counter > zero_counter:
                if "1" in dashed_node.domain:
                    dashed_node.domain.remove("1")
        i += 1

    i = 0
    while i < number_of_rows:
        dash_counter = 0
        dashed_cells = []
        j = 0
        while j < number_of_rows:
            if input_matrix[j][i] == "-":
                dash_counter += 1
                dashed_cells.append(str(j) + "," + str(i))
            j += 1
        if dash_counter == 1:
            k = 0
            while k < len(nodes):
                if nodes[k].id == dashed_cells[0]:
                    dashed_node = nodes[k]
                    break
                k += 1
            one_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[j][i] == "1":
                    one_counter += 1
                j += 1
            zero_counter = 0
            j = 0
            while j < number_of_rows:
                if input_matrix[j][i] == "0":
                    zero_counter += 1
                j += 1
            if zero_counter > one_counter:
                if "0" in dashed_node.domain:
                    dashed_node.domain.remove("0")
            if one_counter > zero_counter:
                if "1" in dashed_node.domain:
                    dashed_node.domain.remove("1")
        i += 1


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

            # Checking more than row equal numbers in a column constraint
            if row - 1 >= 0 and row + 1 < number_of_rows and input_matrix[row - 1][column] == input_matrix[row + 1][column] and input_matrix[row - 1][column] != "-":
                value = input_matrix[row - 1][column]
                if value in node.domain:
                    node.domain.remove(value)
            if row - 2 >= 0 and input_matrix[row - 2][column] == input_matrix[row - 1][column] and input_matrix[row - 2][column] != "-":
                value = input_matrix[row - 2][column]
                if value in node.domain:
                    node.domain.remove(value)
            if row + 2 < number_of_rows and input_matrix[row + 2][column] == input_matrix[row + 1][column] and input_matrix[row + 2][column] != "-":
                value = input_matrix[row + 2][column]
                if value in node.domain:
                    node.domain.remove(value)

            # Checking more than row equal numbers in a row constraint
            if column - 1 >= 0 and column + 1 < number_of_rows and input_matrix[row][column - 1] == input_matrix[row][column + 1] and input_matrix[row][column - 1] != "-":
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


# This function checks if the number of ones in each row of the input matrix is equal to input number or not
def number_of_ones_checker(input_matrix, input_number, number_of_rows):
    for i in input_matrix:
        one_counter = 0
        for j in i:
            if j == "1":
                one_counter += 1
        if one_counter != input_number:
            return False

    i = 0
    while i < number_of_rows:
        j = 0
        one_counter = 0
        while j < number_of_rows:
            if input_matrix[j][i] == "1":
                one_counter += 1
            j += 1
        if one_counter != input_number:
            return False
        i += 1
    return True


# This function prints the input matrix
def matrix_printer(input_matrix):
    for i in input_matrix:
        line = ""
        for j in i:
            line += j + "    "
        print(line)
    print("=====================================================================")


# This function checks the number of ones and zeros in a row
def row_numbers_checker(input_matrix, number_of_rows):
    i = 0
    while i < number_of_rows:
        j = 0
        while j <= number_of_rows - 3:
            if input_matrix[i][j] == input_matrix[i][j + 1] and input_matrix[i][j + 1] == input_matrix[i][j + 2]:
                return False
            j += 1
        i += 1

    i = 0
    while i < number_of_rows:
        j = 0
        while j <= number_of_rows - 3:
            if input_matrix[j][i] == input_matrix[j + 1][i] and input_matrix[j + 1][i] == input_matrix[j + 2][i]:
                return False
            j += 1
        i += 1
    return True


# The AC_3 algorithm is implemented here
def ac_3(input_nodes, queue, input_matrix, nodes, number_of_rows):
    first_node = input_nodes[0]
    second_node = input_nodes[1]
    first_node_row, first_node_column = row_and_column_finder(first_node.id)
    second_node_row, second_node_column = row_and_column_finder(second_node.id)

    # Checking for row equal values in a row
    if first_node_row == second_node_row:
        if first_node_column + 1 == second_node_column and first_node_column + 2 < number_of_rows and input_matrix[first_node_row][first_node_column + 2] != "-" and second_node.value == input_matrix[first_node_row][first_node_column + 2]:
            print()
            value = input_matrix[first_node_row][first_node_column + 2]
            if value in first_node.domain:
                first_node.domain.remove(value)

                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_column + 2 == second_node_column and first_node_column + 1 < number_of_rows and input_matrix[first_node_row][first_node_column + 1] != "-" and second_node.value == input_matrix[first_node_row][first_node_column + 1]:
            value = input_matrix[first_node_row][first_node_column + 1]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_column - 1 == second_node_column and first_node_column + 1 < number_of_rows and input_matrix[first_node_row][first_node_column + 1] != "-" and second_node.value == input_matrix[first_node_row][first_node_column + 1]:
            value = input_matrix[first_node_row][first_node_column + 1]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_column + 1 == second_node_column and first_node_column - 1 >= 0 and input_matrix[first_node_row][first_node_column - 1] != "-" and second_node.value == input_matrix[first_node_row][first_node_column - 1]:
            value = input_matrix[first_node_row][first_node_column - 1]
            if value in first_node.domain:
                first_node.domain.remove(value)


                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_column - 2 == second_node_column and first_node_column - 1 >= 0 and input_matrix[first_node_row][first_node_column - 1] != "-" and second_node.value == input_matrix[first_node_row][first_node_column - 1]:
            value = input_matrix[first_node_row][first_node_column - 1]
            if value in first_node.domain:
                first_node.domain.remove(value)


                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_column - 1 == second_node_column and first_node_column - 2 >= 0 and input_matrix[first_node_row][first_node_column - 2] != "-" and second_node.value == input_matrix[first_node_row][first_node_column - 2]:
            value = input_matrix[first_node_row][first_node_column - 2]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

    # Checking for row equal values in a column
    if first_node_column == second_node_column:
        if first_node_row + 1 == second_node_row and first_node_row + 2 < number_of_rows and input_matrix[first_node_row + 2][first_node_column] != "-" and second_node.value == input_matrix[first_node_row + 2][first_node_column]:
            value = input_matrix[first_node_row + 2][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)




                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_row + 2 == second_node_row and first_node_row + 1 < number_of_rows and input_matrix[first_node_row + 1][first_node_column] != "-" and second_node.value == input_matrix[first_node_row + 1][first_node_column]:
            value = input_matrix[first_node_row + 1][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)




                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_row - 1 == second_node_row and first_node_row + 1 < number_of_rows and input_matrix[first_node_row + 1][first_node_column] != "-" and second_node.value == input_matrix[first_node_row + 1][first_node_column]:
            value = input_matrix[first_node_row + 1][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])


        if first_node_row + 1 == second_node_row and first_node_row - 1 >= 0 and input_matrix[first_node_row - 1][first_node_column] != "-" and second_node.value == input_matrix[first_node_row - 1][first_node_column]:
            value = input_matrix[first_node_row - 1][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_row - 2 == second_node_row and first_node_row - 1 >= 0 and input_matrix[first_node_row - 1][first_node_column] != "-" and second_node.value == input_matrix[first_node_row - 1][first_node_column]:
            value = input_matrix[first_node_row - 1][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)



                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])

        if first_node_row - 1 == second_node_row and first_node_row - 2 >= 0 and input_matrix[first_node_row - 2][first_node_column] != "-" and second_node.value == input_matrix[first_node_row - 2][first_node_column]:
            value = input_matrix[first_node_row - 2][first_node_column]
            if value in first_node.domain:
                first_node.domain.remove(value)


                for node in nodes:
                    neighbor_row, neighbor_column = row_and_column_finder(node.id)
                    if (not node.assigned) and node.id != first_node.id:
                        if neighbor_row == first_node_row or neighbor_column == first_node_column:
                            queue.append([node, first_node])


# Maintaining arc consistency algorithm is implemented here
def maintaining_arc_consistency(input_matrix, nodes, number_of_rows, last_node):
    queue = []
    last_node_row, last_node_column = row_and_column_finder(last_node.id)
    for node in nodes:
        row, column = row_and_column_finder(node.id)
        if node.id != last_node.id and (not node.assigned):
            if row == last_node_row or column == last_node_column:
                queue.append([node, last_node])

    while len(queue) != 0:
        ac_3(queue[0], queue, input_matrix, nodes, number_of_rows)
        queue.pop(0)



# Main part of the code starts here
input_matrix, number_of_rows, algorithm_number = file_reader()
if algorithm_number == "1":
    forward_checking_start_time = time.time()   # Starting timer
    matrix_printer(input_matrix)
    input_matrix_copy = matrix_copier(input_matrix)
    nodes = nodes_generator(input_matrix, number_of_rows)
    forward_checker(input_matrix, nodes, number_of_rows)
    root = minimum_remaining_value_finder(nodes)
    random_assigner(root)
    row, column = row_and_column_finder(root.id)
    input_matrix[row][column] = root.value
    matrix_printer(input_matrix)
    root.assigned = True
    root.parent = node("1")  # This is the root's parent id for finding it
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
                if error_counter == 20:
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
                    matrix_printer(input_matrix)
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
                matrix_printer(input_matrix)
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
            matrix_printer(input_matrix)
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
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    number_of_assigned_nodes = 1
                    previous_selected_node = root
                    current_node = minimum_remaining_value_finder(nodes)
                    current_node.parent = root
                    error = False
                    continue

                if not number_of_ones_checker(input_matrix, number_of_rows / 2, number_of_rows):
                    input_matrix = input_matrix_copy
                    input_matrix_copy = matrix_copier(input_matrix)
                    nodes = nodes_generator(input_matrix, number_of_rows)
                    forward_checker(input_matrix, nodes, number_of_rows)
                    root = minimum_remaining_value_finder(nodes)
                    random_assigner(root)
                    row, column = row_and_column_finder(root.id)
                    input_matrix[row][column] = root.value
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    number_of_assigned_nodes = 1
                    previous_selected_node = root
                    current_node = minimum_remaining_value_finder(nodes)
                    current_node.parent = root
                    error = False
                    continue

    if not error:
        print("FINAL RESULT: ")
        matrix_printer(input_matrix)
        forward_checking_stop_time = time.time()
        print("Time: " + str(round(forward_checking_stop_time - forward_checking_start_time, 3)) + " s")



if algorithm_number == "2":
    mac_start_time = time.time()    # Starting timer
    matrix_printer(input_matrix)
    input_matrix_copy = matrix_copier(input_matrix)
    nodes = nodes_generator(input_matrix, number_of_rows)
    root = minimum_remaining_value_finder(nodes)
    equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
    if len(root.domain) != 0:
        random_assigner(root)
    else:
        print("Error1")
        exit(0)
    row, column = row_and_column_finder(root.id)
    input_matrix[row][column] = root.value
    matrix_printer(input_matrix)
    root.assigned = True
    root.parent = node("1")  # This is the root's parent id for finding it
    root.domain.remove(root.value)
    maintaining_arc_consistency(input_matrix, nodes, number_of_rows, root)
    number_of_assigned_nodes = 1
    counter = 0
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
                if error_counter == 400:
                    print("Error2")
                    error = True
                    break
                else:
                    input_matrix = input_matrix_copy
                    input_matrix_copy = matrix_copier(input_matrix)
                    nodes = nodes_generator(input_matrix, number_of_rows)
                    root = minimum_remaining_value_finder(nodes)
                    equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
                    if len(root.domain) != 0:
                        random_assigner(root)
                    else:
                        print("Error3")
                        exit(0)
                    row, column = row_and_column_finder(root.id)
                    input_matrix[row][column] = root.value
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    maintaining_arc_consistency(input_matrix, nodes, number_of_rows, root)
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
                matrix_printer(input_matrix)
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
            if number_of_assigned_nodes != len(nodes):
                equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
            if len(current_node.domain) == 0:
                counter += 1
                if counter >= 20000:

                    print("Error4")
                    exit(0)
                continue
            random_assigner(current_node)
            row, column = row_and_column_finder(current_node.id)
            input_matrix[row][column] = current_node.value
            matrix_printer(input_matrix)
            current_node.assigned = True
            number_of_assigned_nodes += 1
            current_node.domain.remove(current_node.value)
            maintaining_arc_consistency(input_matrix, nodes, number_of_rows, current_node)
            current_node.parent = previous_selected_node
            previous_selected_node = current_node
            current_node = minimum_remaining_value_finder(nodes)
            if number_of_assigned_nodes == len(nodes):
                row_strings = row_strings_finder(input_matrix, number_of_rows)
                column_strings = column_strings_finder(input_matrix, number_of_rows)
                if does_repetition_exist(row_strings) or does_repetition_exist(column_strings):
                    input_matrix = input_matrix_copy
                    input_matrix_copy = matrix_copier(input_matrix)
                    nodes = nodes_generator(input_matrix, number_of_rows)
                    root = minimum_remaining_value_finder(nodes)
                    equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
                    if len(root.domain) != 0:
                        random_assigner(root)
                    else:
                        print("Error5")
                        exit(0)
                    row, column = row_and_column_finder(root.id)
                    input_matrix[row][column] = root.value
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    maintaining_arc_consistency(input_matrix, nodes, number_of_rows, root)
                    number_of_assigned_nodes = 1
                    previous_selected_node = root
                    current_node = minimum_remaining_value_finder(nodes)
                    current_node.parent = root
                    error = False
                    continue

                if not number_of_ones_checker(input_matrix, number_of_rows / 2, number_of_rows):
                    input_matrix = input_matrix_copy
                    input_matrix_copy = matrix_copier(input_matrix)
                    nodes = nodes_generator(input_matrix, number_of_rows)
                    root = minimum_remaining_value_finder(nodes)
                    equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
                    if len(root.domain) != 0:
                        random_assigner(root)
                    else:
                        print("Error6")
                        exit(0)
                    row, column = row_and_column_finder(root.id)
                    input_matrix[row][column] = root.value
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    maintaining_arc_consistency(input_matrix, nodes, number_of_rows, root)
                    number_of_assigned_nodes = 1
                    previous_selected_node = root
                    current_node = minimum_remaining_value_finder(nodes)
                    current_node.parent = root
                    error = False
                    continue
                if not row_numbers_checker(input_matrix, number_of_rows):
                    input_matrix = input_matrix_copy
                    input_matrix_copy = matrix_copier(input_matrix)
                    nodes = nodes_generator(input_matrix, number_of_rows)
                    root = minimum_remaining_value_finder(nodes)
                    equal_zeros_and_ones_checker(nodes, input_matrix, number_of_rows)
                    if len(root.domain) != 0:
                        random_assigner(root)
                    else:
                        print("Error7")
                        exit(0)
                    row, column = row_and_column_finder(root.id)
                    input_matrix[row][column] = root.value
                    matrix_printer(input_matrix)
                    root.assigned = True
                    root.parent = node("1")
                    root.domain.remove(root.value)
                    maintaining_arc_consistency(input_matrix, nodes, number_of_rows, root)
                    number_of_assigned_nodes = 1
                    previous_selected_node = root
                    current_node = minimum_remaining_value_finder(nodes)
                    current_node.parent = root
                    error = False
                    continue





    if not error:
        print("FINAL RESULT: ")
        matrix_printer(input_matrix)
        mac_stop_time = time.time()
        print("Time: " + str(round(mac_stop_time - mac_start_time, 3)) + " s")








