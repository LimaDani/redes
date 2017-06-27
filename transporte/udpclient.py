# Camada de Transporte - Cliente UDP 

import socket
import sys
import subprocess

# Criando um socket TCP/IP 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Conectando o socket a porta onde o servidor esta escutando
server_address = (sys.argv[1], 10000)
print >>sys.stderr, 'Conectando a %s porta %s' % server_address

try:
    
    # Chamando a Camada Fisica
    subprocess.check_output(['./client', sys.argv[1], sys.argv[2]])
    print >>sys.stderr, 'Envio de Transporte para Fisica'

finally:
    print >>sys.stderr, 'Fechando socket Cliente UDP'
