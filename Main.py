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


# This function generates a dictionary of values and variables for the variables which do not have values
def variables_values_dictionary_generator(input_matrix, input_number_of_rows):
    variables_values = {}
    i = 0
    while i < input_number_of_rows:
        j = 0
        while j < input_number_of_rows:
            if input_matrix[i][j] == '-':
                key = str(i) + "," + str(j)
                variables_values[key] = ["0", "1"]
            j += 1
        i += 1
    return variables_values



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




# Forward chking part of the algorithm is implemented here
def forward_checker(input_matrix, variables_values):
    # The equal number of zeros and ones in each row and column is implemented here
    for key in variables_values:
        row, column = row_and_column_finder(key)












# Main part of the code starts here
input_matrix, number_of_rows = file_reader()
print(input_matrix)

variables_values = variables_values_dictionary_generator(input_matrix, number_of_rows)


forward_checker(input_matrix, variables_values)



























