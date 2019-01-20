svastica = """
😇🅱🅱😇😇😇😇
😇🅱🅱😇🅱🅱🅱
😇🅱🅱😇🅱🅱🅱
😇😇😇😇😇😇😇
🅱🅱🅱😇🅱🅱😇
🅱🅱🅱😇🅱🅱😇
😇😇😇😇🅱🅱😇
"""


allowed_users = {"longo", "notario", "iuculano", "francescone", "di stefano"}
admins = {"longo"}


tracotante_answers = [svastica, 'L\'aggettivo per *antonomasia*', '*SILENZIO ITTICO*', "ASILO MARIUCCIA, SIAMO ALL\'ASILO MARIUCCIA"]

help_msg = """
*🌐Comandi disponibili:*
*!xp:* mostra il valore attuale dei tuoi XP
*!xp [cognome]:* mostra il valore attuale degli XP di qualcun'altro
*!comandi:* Mostra questo messaggio
*!tracotante:* AUA
*!insulta [nome]:* Centinaia di insulti per mamme zii e cugini di chiunque
*!lista:* Crea una lista randomica tra gli utenti del gruppo
"""

insulti = [
"%s tua madre è come un cuore, se non batte muore",
"%s sei simpatico come un grappolo di emorroidi",
"%s sei utile come un culo senza il buco",
"%s tua madre è così grassa che è stata usata come controfigura dell'iceberg in Titanic",
"%s hai il buco del culo con lo stesso diametro del traforo della manica",
]



class UserNotExists(Exception):
    pass
class NotACommand(Exception):
    pass
class PermissionDenied(Exception):
    pass
