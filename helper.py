from vars import NotACommand
from difflib import get_close_matches

def is_command(message: str, prefix: str="!") -> bool:
    """
    return true if @message starts with @prefix
    @params:
    message: the string to check if it's a command
    prefix optional: command prefix
    """
    return message.startswith(prefix)

def has_numbers(val: str):
    return any(char.isdigit() for char in val)

def get_args(message: str, prefix: str="!") -> list:
    """
    returns args from raw message
    @params:
    message: the string to check if it's a command
    prefix optional: command prefix
    """
    if is_command(message):
        a = message.lower()
        list = a[1::].split(" ")
        if len(list) == 4:
            return [list[0], list[1] + " " + list[2], list[3]]
        elif len(list) == 3 and has_numbers(list[2]) == False:
            return [list[0], list[1] + " " + list[2]]


        else:
            return list
    else:
        raise NotACommand

def is_safe(message):
    return message == str


def normalize_list(input):
    output = list()
    for x,row in enumerate(input):
    	output.append(input[x][0])
    return output

if __name__ == "__main__":
    while True:
        if input("Test a function(get_args or is_command): ") == "is_command":
            print(is_command(input("input: "), input("prefix: ")))
        else:
            print(get_args(input("(get_args) string: ")))
