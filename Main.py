
def is_number(input_char):
    if input_char == "0" or input_char == "1" or input_char == "2" or input_char == "3" or input_char == "4" or input_char == "5" or input_char == "6" or input_char == "7" or input_char == "8" or input_char == "9":
        return True
    else:
        return False


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
    return input_matrix




# Main part of the code starts here
input_matrix = file_reader()
print(input_matrix)




























