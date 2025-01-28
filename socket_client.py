import socket
import datetime
import base64
from base58 import b58decode
import re
from dotenv import load_dotenv
import os

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

def flag1(conn):
    """
    Répond à la première question (nom/prénom/classe).
    """
    try:
        response = "alexandre/uzan/3si2"
        conn.sendall(response.encode())
        print(f"Réponse envoyée : {response}")
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
        return wait_server(conn)

    except Exception as e:
        print(f"Erreur dans le traitement de flag5 : {e}")
        return None
    
    
def flag6(conn, statement):
    """
    Traite la question 6 : décodage d'un message en Braille.
    """
    try:
        # On extrait le message hexadécimal
        cleanAnswer = statement.split(" ")[-1].strip()
        print(f"Message hexadécimal : {cleanAnswer}")

        # Convertir de l'hexadécimal en texte
        decodedAnswer = bytes.fromhex(cleanAnswer).decode('utf-8')
        print(f"Message décodé en Braille Unicode : {decodedAnswer}")

        # Convertir du Braille Unicode en texte
        finalAnswer = decode_braille(decodedAnswer)
        print(f"Message final décodé : {finalAnswer}")

        conn.sendall(finalAnswer.encode())
        print(f"Réponse envoyée : {finalAnswer}")
        return wait_server(conn), finalAnswer
    except Exception as e:
        print(f"Erreur inattendue dans flag6 : {e}")
        return None


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

    finally:
        conn.close()
        print("Connexion fermée.")



if __name__ == "__main__":
    main()
