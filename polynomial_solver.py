import re
import numpy as np
import socket

def extract_coefficients(equation):
    coefficients = []
    coeff_strings = re.findall('([+-]? ?\d+)', equation)
    return float(coeff_strings[0].replace(' ','')), float(coeff_strings[1].replace(' ','')), (float(coeff_strings[2].replace(' ','')) - float(coeff_strings[3].replace(' ','')))

def solve_quadratic_equation(a, b, c):
    roots = np.roots([a,b,c])
    roots = [root for root in roots if np.isreal(root) and abs(root) > 1e-6]
    if len(roots) == 0:
        return 'Not possible'
    elif len(roots) == 1:
        return 'x: '  + str(round(roots[0],3))
    else:
        return 'x1: ' + str(round(roots[0],3)) + ' ; x2: ' + str(round(roots[1],3))

# Création de la socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
HOST = 'challenge01.root-me.org'
PORT = 52018
s.connect((HOST, PORT))

# Reception de la réponse
response = s.recv(1000).decode()
print(response)

i=1
while i<=25 :
	# Récupération de l'équation à partir de la réponse
	polynome = re.search(r'Solve this equation please: (.*)', response).group(1)
	a, b, c = extract_coefficients(polynome)
	message = solve_quadratic_equation(a, b, c)

	print(message)
	# Envoi de la réponse à l'équation
	message+='\n'
	s.send(message.encode())

	# Réception de la réponse
	response = s.recv(1000).decode()
	print(response)
	i+=1

# Fermeture de la socket
s.close()

