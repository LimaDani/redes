# Camada de Transporte - ServidorUDP 

import socket
import sys
import subprocess

try:
    
    # Chamando a Camada de Aplicacao
    subprocess.check_output(["ruby" , "server.rb"])
    print >>sys.stderr, 'Envio de Transporte para Aplicacao'

finally:
    print >>sys.stderr, 'Fechando socket Servidor UDP'
