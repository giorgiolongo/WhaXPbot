from helper import *
from db import *
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
import mysql.connector
import random
from data import *
from time import sleep
from pprint import pprint
import traceback
from difflib import get_close_matches
from dateparser import parse
import datetime

driver = WhatsAPIDriver(loadstyles=False, profile="/home/bot/z5vhmp3k.WhaXPbot/")
pause = False
homeworkreq = ["","",""]
print("Python: Bot Started.")
try:
    if __name__ == "__main__":
        while True:
            for contact in driver.get_unread():
                for message in contact.messages:
                    try:
                        if message.sender.name == homeworkreq[0]:
                            AddHomework(homeworkreq[2], homeworkreq[1], message.content)
                            contact.chat.send_message("✅Compiti aggiungi")
                            homeworkreq = ["","",""]
                            pass

                        if pause == True and is_command(message.content) and get_args(message.content)[0] == "riprendi":
                            if message.sender.name in allowed_users:
                                contact.chat.send_message("▶Bot nuovamente attivo")
                                pause = False
                                continue

                        if isinstance(message, Message) and is_command(message.content) and pause == False and message.sender.name not in banned:
                            #pprint(vars(contact))
                            #pprint(vars(message))
                            #driver.chat_reply_message("false_393426264750@c.us_AB38088B2841A6BC4795CC07E8DCF135", "aua")
                            if get_args(message.content)[0] in textcommands.keys():
                                contact.chat.send_message(simple_command_hendler(message.content))
                                #----------------------------!xp------------------------------#
                            elif get_args(message.content)[0] == "xp":  #!xp command
                                if len(get_args(message.content)) == 1:
                                    contact.chat.send_message("I tuoi Xp attuali: " + str(XPdump(str(message.sender.name), cursor, database)[0]))
                                elif len(get_args(message.content)) == 2:
                                    answer = XPdump(str(get_args(message.content)[1]), cursor, database)
                                    contact.chat.send_message(answer[1] + " ha attualmente " + answer[0] + "XP")
                                elif len(get_args(message.content)) == 3:
                                    if message.sender.name in allowed_users:
                                        answer = XPupdate(str(get_args(message.content)[1]), int(get_args(message.content)[2]), cursor, database)
                                        contact.chat.send_message(str(get_args(message.content)[2]) + " XP a " + answer[1] + "\nXP totali: " + answer[0])
                                    else:
                                        raise PermissionDenied
                            elif get_args(message.content)[0] == "lista": #!randomize <pair by>
                                if len(get_args(message.content)) > 2:
                                    reply = "*Lista di " + get_args(message.content)[1] + "* \n"
                                userlist = [x.capitalize() for x in GetList()]
                                reply += "\n".join(random.sample(userlist, len(GetList())))
                                contact.chat.send_message(reply)
                            elif get_args(message.content)[0] == "classifica": #!randomize <pair by>
                                contact.chat.send_message(stringify_leaderboard(scoreboard()))

                            #----------------------------!compiti---------------------------#
                            elif get_args(message.content)[0] == "compiti":
                                args = split_by_word(message.content, ["di", "per"], ["il"])
                                if len(get_args(message.content)) == 1:
                                    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                                    date = tomorrow.strftime('%d/%m/%Y')
                                    contact.chat.send_message(stringify_homework(DumpHomewok(date), date))
                                elif len(args) == 2:
                                    dateval = parse(args[1], languages=['it'], settings={'TIMEZONE': '+0100','PREFER_DATES_FROM': 'future'}).date()
                                    date = dateval.strftime('%d/%m/%Y')
                                    contact.chat.send_message(stringify_homework(DumpHomewok(date), date))

                                elif len(args) == 3:
                                    dateval = parse(args[2], languages=['it'], settings={'TIMEZONE': '+0100','PREFER_DATES_FROM': 'future'}).date()
                                    date = dateval.strftime('%d/%m/%Y')
                                    homeworkreq = [message.sender.name, get_close_matches(args[1], subjectslist, n=1, cutoff=0.5)[0], date]
                                    contact.chat.send_message("✅Invia ora i compiti in un messaggio unico:")
                                else:
                                    raise CmdSyntaxError

                            elif get_args(message.content)[0] == "pausa":
                                if message.sender.name in admins:
                                    contact.chat.send_message("⏸Bot in pausa")
                                    pause = True
                                else:
                                    raise PermissionDenied
                            elif get_args(message.content)[0] == "riavvia":
                                if message.sender.name in admins:
                                    contact.chat.send_message("🔁Riavvio bot in corso...")
                                    driver.quit()
                                    quit()
                                else:
                                    raise PermissionDenied
                            #Error
                            else:
                                raise NotACommand
                    except AttributeError:
                        pass
                    except UserNotExists:
                        contact.chat.send_message("❌Utente non trovato")
                        pass
                    except PermissionDenied:
                        contact.chat.send_message("❌Non hai i permessi per utilizzare questo comando")
                        pass
                    except NotACommand:
                        contact.chat.send_message("❌Comando non disponibile, !comandi per tutti i comandi disponibili")
                        pass
                    except CmdSyntaxError:
                        contact.chat.send_message("❌Sintassi comando errata")
                        pass
                    except mysql.connector.errors.DatabaseError:
                        database.reconnect()
                        cursor = database.cursor(buffered=True)
                        contact.chat.send_message("🕜Il bot è stato inattivo per troppo tempo: Esegui nuovamente il comando.")
                        traceback.print_exc()
                        pass
                    except:
                        traceback.print_exc()
                        contact.chat.send_message("❌C'è stato un errore")
except KeyboardInterrupt:
    quit()
except:
    traceback.print_exc()
