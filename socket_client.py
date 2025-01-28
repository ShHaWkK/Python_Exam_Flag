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


def wait_answer(conn):
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



def flag1(conn):
    """
    Répond à la première question (nom/prénom/classe).
    """
    try:
        response = "alexandre/uzan/3si2"
        conn.sendall(response.encode())
        print(f"Réponse envoyée : {response}")
        return wait_answer(conn)
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
        return wait_answer(conn)
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
        return wait_answer(conn)

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
        return wait_answer(conn)

    except ValueError as ve:
        print(f"Erreur : {ve}")
        return None
    except Exception as e:
        print(f"Erreur inattendue dans flag4 : {e}")
        return None



def main():
    """
    Exécute les étapes pour répondre aux questions.
    """
    conn = connexion()
    try:
        print("---- Récupération des FLAGS ----")
        flag1_result = flag1(conn)
        if not flag1_result:
            raise Exception("Erreur dans le traitement de flag1")

        flag2_result = flag2(conn)
        if not flag2_result:
            raise Exception("Erreur dans le traitement de flag2")

        flag3_result = flag3(conn, flag2_result)
        if not flag3_result:
            print("Erreur : Impossible de résoudre Flag 3. Passage au suivant.")
            flag4_result = None
        else:
            flag4_result = flag4(conn, flag3_result)

        print("\nRécapitulatif des FLAGS :")
        print(f"FLAG 1 : {flag1_result}")
        print(f"FLAG 2 : {flag2_result}")
        print(f"FLAG 3 : {flag3_result}")
        print(f"FLAG 4 : {flag4_result}")
    finally:
        conn.close()
        print("Connexion fermée.")


if __name__ == "__main__":
    main()
