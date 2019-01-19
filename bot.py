from helper import get_args, is_command
from db import XPdump, XPupdate, GetList
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
import mysql.connector
import random
import traceback
from vars import *

database = mysql.connector.connect(
  host="192.168.1.3",
  user="pi",
  passwd="raspberry",
  auth_plugin='mysql_native_password',
  port="3306",
  database="xp"
)
cursor = database.cursor(buffered=True)

driver = WhatsAPIDriver(loadstyles=True)
print("Waiting for QR")
driver.wait_for_login()
pause = False
try:
    if __name__ == "__main__":
        while True:
            for contact in driver.get_unread():
                for message in contact.messages:
                    try:
                        if pause == True and is_command(message.content) and get_args(message.content)[0] == "riprendi":
                            if message.sender.name in allowed_users:
                                contact.chat.send_message("▶Bot nuovamente attivo")
                                pause = False
                                continue

                        if isinstance(message, Message) and is_command(message.content) and pause == False: 


                            if get_args(message.content)[0] == "xp":  #!xp command

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


                            elif get_args(message.content)[0] == "comandi": #!help msg
                                contact.chat.send_message(help_msg)

                            elif get_args(message.content)[0] == "lista": #!randomize <pair by>
                                userlist = [x.capitalize() for x in GetList()]
                                reply = "\n".join(random.sample(userlist, len(GetList())))
                                contact.chat.send_message(reply)

                            elif get_args(message.content)[0] == "insulta": #!insulta cmd
                                persona = get_args(message.content)[1]
                                insulto = random.choice(insulti)
                                contact.chat.send_message(insulto.replace("%s", persona))

                            elif get_args(message.content)[0] == "pausa":
                                if message.sender.name in admins:
                                    contact.chat.send_message("⏸Bot in pausa")
                                    pause = True
                                else:
                                    raise vars.PermissionDenied
                            elif get_args(message.content)[0] == "arresta":
                                if message.sender.name in admins:
                                    contact.chat.send_message("❌Bot arrestato")
                                    driver.quit()
                                    quit()
                                else:
                                    raise PermissionDenied


                            #elif get_args(message.content)[0] == "dump":
                            #    #log.debug(XPdump(get_args(message)[1]))
                            #    contact.chat.send_message("Valore XP attuale: " + str(XPdump(str(get_args(message.content)[1]), cursor, database)))


                            elif get_args(message.content)[0] == "tracotante":      #!tracotante
                                contact.chat.send_message(random.choice(tracotante_answers))
                            #Error
                            else:
                                contact.chat.send_message("Comando non disponibile, !comandi per tutti i comandi disponibili")
                    except AttributeError:
                        pass
                    except UserNotExists:
                        contact.chat.send_message("❌Utente non trovato")
                        pass
                    except PermissionDenied:
                        contact.chat.send_message("❌Non hai i permessi per utilizzare questo comando")
                        pass
                    except NotACommand:
                        pass
                    except:
                        traceback.print_exc()
                        contact.chat.send_message("❌C'è stato un errore")
except KeyboardInterrupt:
    quit()
except:
    traceback.print_exc()
