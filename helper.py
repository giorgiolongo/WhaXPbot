from data import NotACommand, textcommands
from difflib import get_close_matches
import random
from re import split, sub

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

def split_by_word(message, words, bannedwords, remspaces=True):
    wordstr = ""
    bannedstr = ""
    for x,row in enumerate(words):
        wordstr += words[x] + "|"
    for x,row in enumerate(bannedwords):
        bannedstr += bannedwords[x] + "|"
    splitted = split(wordstr[:-1], message)
    if remspaces:
        bannedstr += "\s+"
    for x,row in enumerate(splitted):
        splitted[x] = sub(bannedstr,"", splitted[x])
    return splitted


def stringify_leaderboard(list):
    output = "*👑 Classifica 👑*\n"
    for x,row in enumerate(list):
        name = list[x][0].capitalize()
        y = x + 1
        string = "*" + str(y) + ". " + name + ":* " + str(list[x][1]) + "\n"
        output += string
    return output

def stringify_homework(list, date):
    output = "*📚Compiti per il " + date + ":📚*\n"
    for x,row in enumerate(list):
        name = list[x][0].capitalize()
        output += "*" + name + ":* " + list[x][1] + "\n"
    return output


def normalize_list(input):
    return [i[0] for i in input]

def simple_command_hendler(input):
    answ = random.choice(textcommands[get_args(input)[0]])
    if len(get_args(input)) > 1:
        return answ.replace("%s", get_args(input)[1])
    else:
        return answ
