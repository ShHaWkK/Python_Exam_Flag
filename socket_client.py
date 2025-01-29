import socket
import datetime
import base64
import webcolors
from base58 import b58decode
import re
from dotenv import load_dotenv
import os

reponses = {}

def connexion():
    """
    Établit une connexion au serveur.
    :return: socket
    """
    load_dotenv()
    host = os.getenv("IP_SERVER")
    port = os.getenv("PORT_SERVER")

    if not port.isdigit():
        raise ValueError(f"Le port spécifié {port} n'est pas valide.")
    port = int(port)

    try:
        print("----------------------------------------")
        print(f"Connexion au serveur {host}:{port}")
        print("----------------------------------------")
        connect = socket.create_connection((host, port), timeout=10)
        response = connect.recv(1024).decode()
        print(response)
        return connect
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        exit()


def wait_server(conn):
    """
    Attend et retourne la réponse du serveur.
    """
    try:
        response = conn.recv(1024).decode().strip()
        print(response)
        return response
    except Exception as e:
        print(f"Erreur inattendue lors de la réception : {e}")
        exit()



def decodage(message):
    """
    Décodage du message en Base64, Base32, Base58 ou Base85.
    """
    decoders = {
        'base64': base64.b64decode,
        'base32': base64.b32decode,
        'base85': base64.b85decode,
        'base58': b58decode
    }
    # C'est une boucle qui va essayer de décoder le message
    for encoding, decoder in decoders.items():
        try:
            decoded = decoder(message).decode('utf-8')
            print(f"{encoding} décodé : {decoded}")
            return decoded
        except Exception:
            continue
    print("Impossible de décoder le message.")
    return None


def solve_math_expression(statement):
    """
    Résout une expression mathématique simple.
    """
    try:
        # Extraction de l'expression mathématique à partir du statement
        match = re.search(r"résultat de ([\d\s\+\-\*/]+)\s*\?", statement)
        if not match:
            print("Erreur : Expression mathématique non trouvée dans la question.")
            return None

        expression = match.group(1).strip()
        print(f"Expression détectée : {expression}")
        """
        J'ai utilisé eval pour évaluer l'expression mathématique.
        C'est à dire que si l'expression est "2 + 2", eval renverra 4.
        
        """
        result = eval(expression)
        return int(result) 
    except Exception as e:
        print(f"Erreur dans le calcul de l'expression mathématique : {e}")
        return None


MORSE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9'
}

"""
Flag 6 
"""


def decode_braille(braille):
    """Convertit le Braille Unicode en texte clair, gère les espaces et ignore les caractères inconnus."""
    brailleDict = {
        '\u2801': 'a', '\u2803': 'b', '\u2809': 'c', '\u2819': 'd', '\u2811': 'e',
        '\u280b': 'f', '\u281b': 'g', '\u2813': 'h', '\u280a': 'i', '\u281a': 'j',
        '\u2805': 'k', '\u2807': 'l', '\u280d': 'm', '\u281d': 'n', '\u2815': 'o',
        '\u280f': 'p', '\u281f': 'q', '\u2817': 'r', '\u280e': 's', '\u281e': 't',
        '\u2825': 'u', '\u2827': 'v', '\u283a': 'w', '\u282d': 'x', '\u283d': 'y',
        '\u2835': 'z', '\u2821': ' ',
        '\u2800': '1', '\u2802': '2', '\u2804': '3', '\u2806': '4', '\u2808': '5',
        '\u2810': '6', '\u2812': '7', '\u2814': '8', '\u2816': '9', '\u2818': '0',
        '\u2820': '!', '\u280c': '-', '\u2808': '?', '\u2804': '.', '\u2806': "'", '\u281c': ',',
    }

    decoded_message = []

    for char in braille:
        if char in brailleDict:
            decoded_message.append(brailleDict[char])
            # On va ignorer l'espace
        elif char == ' ':
            continue
        else:
            print(f"Caractère inconnu ignoré : {repr(char)}")
            continue

    return ''.join(decoded_message).upper()


def get_color_name(rgb_tuple):
    """
    Cette fonction sert à trouver le nom de la couleur correspondant aux valeurs RGB.
    """
    try:
        return webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        closest_color = min(webcolors.CSS3_NAMES_TO_HEX,
                            key=lambda name: sum((c1 - c2) ** 2 for c1, c2 in zip(webcolors.hex_to_rgb(webcolors.CSS3_NAMES_TO_HEX[name]), rgb_tuple)))
        return closest_color

def flag1(conn):
    """
    Répond à la première question (nom/prénom/classe).
    """
    try:
        response = "alexandre/uzan/3si2"
        conn.sendall(response.encode())
        print(f"Réponse envoyée : {response}")
        reponses["1"] = response
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")


def flag2(conn):
    """
    Répond à la question sur la date du jour.
    """
    try:
        today = datetime.datetime.now().strftime("%d/%m")
        conn.sendall(today.encode())
        print(f"Réponse envoyée : {today}")
        reponses["2"] = today
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")


def flag3(conn, statement):
    """
    Résout une expression mathématique simple.
    """
    try:
        if "résultat de" not in statement:
            print("Erreur : L'expression mathématique attendue n'a pas été trouvée.")
            return None

        # Extraction propre de l'expression
        clean_answer = statement.split("résultat de ")[1].split(" ?")[0]
        operand1, operator, operand2 = clean_answer.split(" ")
        print(f"Calcul : {operand1} {operator} {operand2}")

        # Calcul basé sur l'opérateur
        if operator == "+":
            result = int(operand1) + int(operand2)
        elif operator == "-":
            result = int(operand1) - int(operand2)
        elif operator == "*":
            result = int(operand1) * int(operand2)
        else:
            raise ValueError("Opérateur inconnu")

        # Envoi du résultat
        conn.sendall(str(result).encode())
        print(f"Résultat envoyé : {result}")
        reponses["3"] = result
        return wait_server(conn)

    except ValueError as ve:
        print(f"Erreur dans le traitement de l'opération mathématique : {ve}")
        return None
    except Exception as e:
        print(f"Erreur inattendue dans flag3 : {e}")
        return None


def flag4(conn, statement):
    """
    Décodage du message pour la question 4.
    """
    try:
        if not statement:
            print("Erreur : La question pour flag4 est vide ou invalide.")
            return None
        encoded_message = statement.split(" ")[-1].strip()
        print(f"Message encodé détecté : {encoded_message}")

        decoded_message = decodage(encoded_message)
        if not decoded_message:
            raise ValueError("Impossible de décoder le message.")

        conn.sendall(decoded_message.encode())
        print(f"Message décodé envoyé : {decoded_message}")
        reponses["4"] = decoded_message
        return wait_server(conn)

    except ValueError as ve:
        print(f"Erreur : {ve}")
        return None
    except Exception as e:
        print(f"Erreur inattendue dans flag4 : {e}")
        return None

def flag5(conn, statement):
    """
    Décoder un message en morse donné en hexadécimal et répondre en majuscules.
    """
    try:
        #Extraire le message hexadécimal
        hex_message = statement.split(":")[-1].strip()
        print(f"Message hexadécimal : {hex_message}")

        #Décoder de l'hexadécimal en morse
        morse_message = bytes.fromhex(hex_message).decode('utf-8')
        print(f"Message morse : {morse_message}")

        #Convertir le morse en texte
        """
        On met les mots dans une liste, 
        puis on les sépare par 2 espaces pour les mots et 1 espace pour les lettres.
        """
        words = morse_message.split("  ")
        decoded_message = []
        for word in words:
            letters = word.split(" ")
            decoded_word = ''.join(MORSE_DICT.get(letter, '?') for letter in letters)
            decoded_message.append(decoded_word)
        final_message = ' '.join(decoded_message).upper()

        print(f"Message décodé : {final_message}")

        conn.sendall(final_message.encode())
        print(f"Réponse envoyée : {final_message}")
        reponses["5"] = final_message
        return wait_server(conn)

    except Exception as e:
        print(f"Erreur dans le traitement de flag5 : {e}")
        return None
    
    
def flag6(conn, statement):
    """
    Traite la question 6 : décodage d'un message en Braille.
    """
    try:
        """
        Explication de la fonction : 
        Tout d'abord, j'ai extrait le message hexadécimal de la question.
        Ensuite, j'ai converti le message hexadécimal en texte.
        J'ai ensuite converti le texte en Braille Unicode.
        Enfin, j'ai converti le Braille Unicode en texte clair avec l'aide de la fonction decode_braille.
        
        """
        cleanAnswer = statement.split(" ")[-1].strip()
        print(f"Message hexadécimal : {cleanAnswer}")

        decodedAnswer = bytes.fromhex(cleanAnswer).decode('utf-8')
        print(f"Message décodé en Braille Unicode : {decodedAnswer}")

        finalAnswer = decode_braille(decodedAnswer)
        print(f"Message final décodé : {finalAnswer}")

        conn.sendall(finalAnswer.encode())
        print(f"Réponse envoyée : {finalAnswer}")
        reponses["6"] = finalAnswer
        return wait_server(conn), finalAnswer
    except Exception as e:
        print(f"Erreur inattendue dans flag6 : {e}")
        return None
    
def flag7(conn, statement):
    """
    Répond à la question 7 concernant la couleur pour les valeurs RGB données.
    """
    try:
        """
        Explication dans ma fonction 
        Tout d'abord, j'ai utilisé une expression régulière pour capturer les valeurs RGB dans la question.
        Ensuite, j'ai converti les valeurs capturées en tuple d'entiers.
        Au début j'avais affiché en hexadécimal les valeurs RGB mais cela ne marchait pas, car il demandait le nom de la couleur en RGB.
        Enfin, j'ai utilisé la fonction get_color_name pour trouver le nom de la couleur aux valeurs RGB.
        """
        match = re.search(r'RGB\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)', statement, re.IGNORECASE)
        if not match:
            raise ValueError(f"Impossible de trouver les valeurs RGB dans la question : {statement}")
        
        rgb_values = tuple(map(int, match.groups()))
        print(f"Valeurs RGB extraites : {rgb_values}")

        color_name = get_color_name(rgb_values)
        print(f"Nom de la couleur : {color_name}")

        conn.sendall(color_name.encode())
        print(f"Réponse envoyée : {color_name}")
        reponses["7"] = color_name
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur inattendue dans flag7 : {e}")
        return None

def flag8(conn, statement):
    """
    Réponds aux questions qui sont passés. 
    """    
    match = re.search(r"réponse de la question (\d+)", statement, re.IGNORECASE)
    if not match:
        print("La question précédente n'a pas été trouvée.")
        return None

    question_number = match.group(1)

    if question_number not in reponses:
        print(f"Réponse pour la question {question_number} non trouvée.")
        return None

    response = str(reponses[question_number])
    conn.sendall(response.encode())
    print(f"Réponse envoyée pour la question {question_number}: {response}")
    return wait_server(conn)


def flag9(conn, statement):
    """
    Comment j'ai réfléchi pour résoudre la question 9
    Tout d'abord, j'ai utilisé une expression régulière pour capturer le numéro du mot et la liste de mots dans la question.
    Ensuite, j'ai vérifié si l'index du mot est valide.
    J'ai ensuite extrait la dernière lettre du mot sélectionné
    Retourne la dernière voyelle du nième mot de la liste 
    """
    try:
        # Extraire le numéro du mot et la liste
        match = re.search(r"dernière lettre du (\d+)[èe]me mot de cette liste: (.+)", statement)
        if not match:
            raise ValueError("Format de la question incorrect.")

        # Récupérer l'index du mot (1-indexé) et la liste de mots
        word_index = int(match.group(1)) - 1
        word_list = match.group(2).split()

        # Vérifier si l'index est valide
        if word_index < 0 or word_index >= len(word_list):
            raise IndexError(f"Index {word_index + 1} hors de portée pour la liste donnée.")

        # Extraire la dernière lettre du mot
        selected_word = word_list[word_index]
        last_letter = selected_word[-1]

        conn.sendall(last_letter.encode())
        print(f"Réponse envoyée : {last_letter}")
        reponses["9"] = last_letter
        return wait_server(conn)

    except (ValueError, IndexError) as e:
        print(f"Erreur dans le traitement de flag9 : {e}")
        conn.sendall("Erreur de traitement".encode())
        return None
    except Exception as e:
        print(f"Erreur inattendue dans flag9 : {e}")
        conn.sendall("Erreur inconnue".encode())
        return None

def flag10(conn):
    """
  Renvoyer toutes vos précédentes réponses, séparer par un underscore (_)
    """
    try:
        answer = "_".join(str(value) for value in reponses.values())
        print("Réponse envoyée : ", answer)
        conn.sendall(answer.encode())
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la réponse : {e}")
        exit()
def main():
    """
    Exécute les étapes pour répondre aux questions.
    """
    conn = connexion()
    try:
        print("---- FLAG ----")
        
        # FLAG 1
        flag1_result = flag1(conn)
        print(f"FLAG 1 : {flag1_result}")

        # FLAG 2
        flag2_result = flag2(conn)
        print(f"FLAG 2 : {flag2_result}")

        # FLAG 3
        flag3_result = flag3(conn, flag2_result)
        print(f"FLAG 3 : {flag3_result}")

        # FLAG 4
        flag4_result = flag4(conn, flag3_result) if flag3_result else None
        print(f"FLAG 4 : {flag4_result}")

        # FLAG 5
        flag5_result = flag5(conn, flag4_result) if flag4_result else None
        print(f"FLAG 5 : {flag5_result}")

        # FLAG 6
        flag6_result = flag6(conn, flag5_result) if flag5_result else None
        print(f"FLAG 6 : {flag6_result}")

        # FLAG 7
        flag7_result = flag7(conn, flag6_result[0]) if flag6_result else None
        print(f"FLAG 7 : {flag7_result}")

        # FLAG 8
        flag8_result = flag8(conn, flag7_result) if flag7_result else None
        print(f"FLAG 8 : {flag8_result}")

        # FLAG 9
        flag9_result = flag9(conn, flag8_result) if flag8_result else None
        print(f"FLAG 9 : {flag9_result}")
        
        # FLAG 10
        flag10_result = flag10(conn)
        print(f"FLAG 10 : {flag10_result}")


    finally:
        conn.close()
        print("Connexion fermée.")



if __name__ == "__main__":
    main()