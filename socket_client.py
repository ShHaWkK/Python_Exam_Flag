import socket
import datetime
import time
import re  # Pour analyser dynamiquement la question

# Informations de connexion
ip = "148.113.42.34"  # Remplacez avec l'IP correcte
port = 24131  # Remplacez avec le bon port

# Fonction pour envoyer et recevoir des données
def communicate(connect, message):
    """
    Envoie un message via le socket et retourne la réponse.
    """
    print(f"Envoi : {message}")
    connect.sendall(message.encode())
    response = connect.recv(1024).decode()
    print(f"Réponse : {response}")
    return response

# Fonction pour résoudre dynamiquement les questions mathématiques
def solve_math_question(question):
    """
    Analyse une question mathématique, extrait les opérandes et l'opérateur,
    et effectue le calcul.
    """
    match = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", question)
    if match:
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))

        # Effectuer l'opération
        if operator == "+":
            return num1 + num2
        elif operator == "-":
            return num1 - num2
        elif operator == "*":
            return num1 * num2
        elif operator == "/":
            return num1 // num2  
    return None

def flag1(connect):
    """
    Répond à la première question pour obtenir le premier FLAG.
    """
    response = communicate(connect, "alexandre/uzan/3si2")
    time.sleep(1)
    if "FLAG" in response:
        first_flag = re.search(r"FLAG\[[^\]]+\]", response).group(0)
        print("Premier FLAG obtenu :", first_flag)
        return first_flag
    return None

def flag2(connect):
    """
    Répond à la deuxième question (date) pour obtenir le deuxième FLAG.
    """
    current_date = datetime.datetime.now().strftime("%d/%m")
    response = communicate(connect, current_date)
    time.sleep(1)
    if "FLAG" in response:
        second_flag = re.search(r"FLAG\[[^\]]+\]", response).group(0)
        print("Deuxième FLAG obtenu :", second_flag)
        return second_flag
    return None

def flag3(connect):
    """
    Résout une question mathématique pour obtenir le troisième FLAG.
    """
    while True:
        response = communicate(connect, "") 
        math_question = response.split("\n")[-1].strip()
        print(f"Question détectée : {math_question}")

        result = solve_math_question(math_question)
        if result is not None:
            response = communicate(connect, str(result))
            if "FLAG" in response:
                third_flag = re.search(r"FLAG\[[^\]]+\]", response).group(0)
                print("Troisième FLAG obtenu :", third_flag)
                return third_flag
        else:
            print("Aucune question mathématique détectée, attente d'une nouvelle réponse.")
            time.sleep(1)

# Main
try:
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.connect((ip, port))
    print("Connexion établie")

    first_flag = flag1(connect)
    second_flag = flag2(connect)
    third_flag = flag3(connect)

finally:
    connect.close()
    print("Connexion fermée")

    print("\nRécapitulatif des FLAGS :")
    print(f"Premier FLAG : {first_flag if first_flag else 'Non obtenu'}")
    print(f"Deuxième FLAG : {second_flag if second_flag else 'Non obtenu'}")
    print(f"Troisième FLAG : {third_flag if third_flag else 'Non obtenu'}")
