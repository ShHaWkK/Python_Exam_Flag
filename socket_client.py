import socket

# Configuration
LOCAL_HOST = "0.0.0.0"  
LOCAL_PORT = 12345 
REMOTE_HOST = "148.113.42.34"
REMOTE_PORT = 51956

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((LOCAL_HOST, LOCAL_PORT))
        print(f"Socket à {LOCAL_HOST} sur le port {LOCAL_PORT}")

        # Connexion au serveur distant
        s.connect((REMOTE_HOST, REMOTE_PORT))
        print(f"Connecté au serveur {REMOTE_HOST} sur le port {REMOTE_PORT}")
        response = s.recv(1024).decode()
        print(f"Question reçue : {response.strip()}")

        """
        Envoi de la réponse au serveur : Alexandre/Uzan/3SI2
        """
        answer = "Alexandre/Uzan/3SI2"
        s.sendall(answer.encode())
        print(f"Réponse envoyé  : {answer}")
        
        # Sortie
        response = s.recv(1024).decode()
        print(f"Réponse du serveur : {response.strip()}")

    except Exception as e:
        print(f"Erreur : {e}")
