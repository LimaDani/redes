# Camada de Transporte - Servidor UDP 

import socket
import sys
import subprocess

f = open('serverlogudp.txt', 'w')
try:
	#Chamando a Camada de Aplicacao
	subprocess.check_output(["ruby" , "server.rb"])
	print >>sys.stderr, 'Envio de Transporte para Aplicacao'
	f.writelines('Envio da camada de Transporte para Aplicacao efetuado\n')
finally:
	f.writelines('Socket do Servidor UDP fechado\n')
	print >>sys.stderr, 'Fechando socket Servidor UDP'
	
