import socket
import datetime
import base64
import webcolors
import re
import os
import string
import nltk

from nltk.corpus import words
from base58 import b58decode
from dotenv import load_dotenv


nltk.download('words')
word_list = set(words.words())

reponses = {}

def connexion():
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
    try:
        response = conn.recv(1024).decode().strip()
        print(response)
        return response
    except Exception as e:
        print(f"Erreur lors de la réception : {e}")
        exit()

def decodage(message):
    decoders = {
        'base64': base64.b64decode,
        'base32': base64.b32decode,
        'base85': base64.b85decode,
        'base58': b58decode
    }
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
    try:
        match = re.search(r"résultat de ([\d\s\+\-\*/]+)\s*\?", statement)
        if not match:
            print("Erreur :Pas le bon format")
            return None

        expression = match.group(1).strip()
        result = eval(expression)
        return int(result) 
    except Exception as e:
        print(f"X Erreur calcul : {e}")
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

def decode_braille(braille):
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
        elif char == ' ':
            continue
        else:
            print(f"inconnu : {repr(char)}")
            continue

    return ''.join(decoded_message).upper()

def get_color_name(rgb_tuple):
    try:
        return webcolors.rgb_to_name(rgb_tuple)
    except ValueError:
        closest_color = min(webcolors.CSS3_NAMES_TO_HEX,
                            key=lambda name: sum((c1 - c2) ** 2 for c1, c2 in zip(webcolors.hex_to_rgb(webcolors.CSS3_NAMES_TO_HEX[name]), rgb_tuple)))
        return closest_color

def decrypt_cesar(text, key):
    alphabet = string.ascii_lowercase
    decrypted_text = []

    for char in text:
        if char in alphabet:
            new_char = alphabet[(alphabet.index(char) - key) % 26]
            decrypted_text.append(new_char)
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

def decrypt_cesar(text, key):
    alphabet = string.ascii_lowercase
    decrypted_text = []

    for char in text:
        if char in alphabet:
            new_char = alphabet[(alphabet.index(char) - key) % 26]
            decrypted_text.append(new_char)
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)


def frequency_analysis(text):
    letter_counts = {char: 0 for char in string.ascii_lowercase}

    for char in text.lower():
        if char in letter_counts:
            letter_counts[char] += 1

    total_letters = sum(letter_counts.values())
    return {char: (count / total_letters) for char, count in letter_counts.items() if total_letters > 0}


def chi_squared_distance(freq1, freq2):
    return sum((freq1.get(letter, 0) - freq2.get(letter, 0))**2 / freq2.get(letter, 0.0001) for letter in string.ascii_lowercase)


def cesar_shift(text):
    best_word = text 
    max_valid_words = 0

    for shift in range(26):
        decrypted_text = decrypt_cesar(text, shift)
        words_found = sum(1 for word in decrypted_text.split() if word.lower() in word_list)

        if words_found > max_valid_words:
            max_valid_words = words_found
            best_word = decrypted_text

    return best_word

def flag1(conn):
    try:
        response = "alexandre/uzan/3si2"
        conn.sendall(response.encode())
        reponses["1"] = response
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur dans l'envoi : {e}")

def flag2(conn):
    try:
        today = datetime.datetime.now().strftime("%d/%m")
        conn.sendall(today.encode())
        reponses["2"] = today
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur dans l'envoi : {e}")

def flag3(conn, statement):
    try:
        if "résultat de" not in statement:
            print("Pas le bon format")
            return None

        clean_answer = statement.split("résultat de ")[1].split(" ?")[0]
        operand1, operator, operand2 = clean_answer.split(" ")

        if operator == "+":
            result = int(operand1) + int(operand2)
        elif operator == "-":
            result = int(operand1) - int(operand2)
        elif operator == "*":
            result = int(operand1) * int(operand2)
        else:
            raise ValueError("Opérateur inconnu")

        conn.sendall(str(result).encode())
        reponses["3"] = result
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur flag3 : {e}")
        return None

def flag4(conn, statement):
    try:
        if not statement:
            print("Erreur : La question est vide ou invalide.")
            return None
        encoded_message = statement.split(" ")[-1].strip()

        decoded_message = decodage(encoded_message)
        if not decoded_message:
            raise ValueError("Impossible de décoder le message.")

        conn.sendall(decoded_message.encode())
        reponses["4"] = decoded_message
        return wait_server(conn)

    except ValueError as ve:
        print(f"Erreur : {ve}")
        return None
    except Exception as e:
        print(f"Erreur flag4 : {e}")
        return None

def flag5(conn, statement):
    try:
        hex_message = statement.split(":")[-1].strip()
        morse_message = bytes.fromhex(hex_message).decode('utf-8')

        words = morse_message.split("  ")
        decoded_message = []
        for word in words:
            letters = word.split(" ")
            decoded_word = ''.join(MORSE_DICT.get(letter, '?') for letter in letters)
            decoded_message.append(decoded_word)
        final_message = ' '.join(decoded_message).upper()

        conn.sendall(final_message.encode())
        reponses["5"] = final_message
        return wait_server(conn)

    except Exception as e:
        print(f"Erreur flag5 : {e}")
        return None

def flag6(conn, statement):
    try:
        cleanAnswer = statement.split(" ")[-1].strip()
        decodedAnswer = bytes.fromhex(cleanAnswer).decode('utf-8')
        finalAnswer = decode_braille(decodedAnswer)

        conn.sendall(finalAnswer.encode())
        reponses["6"] = finalAnswer
        return wait_server(conn), finalAnswer
    except Exception as e:
        print(f"Erreur flag6 : {e}")
        return None

def flag7(conn, statement):
    try:
        match = re.search(r'RGB\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)', statement, re.IGNORECASE)
        if not match:
            raise ValueError(f"trouve pas les valeurs RGB")

        rgb_values = tuple(map(int, match.groups()))
        print(f"Valeurs RGB extraites : {rgb_values}")

        color_name = get_color_name(rgb_values)
        print(f"Nom de la couleur : {color_name}")

        conn.sendall(color_name.encode())
        reponses["7"] = color_name
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur flag7 : {e}")
        return None


def flag8(conn, statement):
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
    reponses["8"] = response

    return wait_server(conn)

def flag9(conn, statement):
    try:
        match = re.search(r"dernière lettre du (\d+)[èe]me mot de cette liste: (.+)", statement)
        if not match:
            raise ValueError("Format de la question incorrecte")

        word_index = int(match.group(1)) - 1
        word_list = match.group(2).split()

        if word_index < 0 or word_index >= len(word_list):
            raise IndexError(f"Index {word_index + 1} hors de portée.")

        selected_word = word_list[word_index]
        last_letter = selected_word[-1]

        conn.sendall(last_letter.encode())
        reponses["9"] = last_letter
        return wait_server(conn)

    except (ValueError, IndexError) as e:
        print(f"Erreur flag9 : {e}")
        conn.sendall("Erreur dans le traitement".encode())
        return None
    except Exception as e:
        print(f"Erreur flag9 : {e}")
        conn.sendall("Erreur inconnue".encode())
        return None

def flag10(conn):
    try:
        ordered_responses = [str(reponses[str(i)]) for i in range(1, 10)]
        answer = "_".join(ordered_responses)

        conn.sendall(answer.encode())
        return wait_server(conn)
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
        exit()

def flag11(conn, statement):
    try:
        # J'extrais le message chiffré
        encrypted_message = statement.split(":")[-1].strip().replace('"', '')
        print(f"Reçoit : {encrypted_message}")
        
        # 
        best_word = cesar_shift(encrypted_message)
        print(f"Envoie : {best_word}")

        conn.sendall(best_word.encode())
        reponses["11"] = best_word
        return wait_server(conn)

    except Exception as e:
        print(f"Erreur lors du décryptage : {e}")
        exit()

def main():
    conn = connexion()
    try:
        flag1_result = flag1(conn)
        flag2_result = flag2(conn)
        flag3_result = flag3(conn, flag2_result)
        flag4_result = flag4(conn, flag3_result) if flag3_result else None
        flag5_result = flag5(conn, flag4_result) if flag4_result else None
        flag6_result = flag6(conn, flag5_result) if flag5_result else None
        flag7_result = flag7(conn, flag6_result[0]) if flag6_result else None
        flag8_result = flag8(conn, flag7_result) if flag7_result else None
        flag9_result = flag9(conn, flag8_result) if flag8_result else None
        flag10_result = flag10(conn)
        flag11_result = flag11(conn, flag10_result)
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()