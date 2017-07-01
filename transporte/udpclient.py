# Camada de Transporte - Cliente UDP 

import socket
import sys
import os
import subprocess

f = open('clientlogudp.txt', 'w')
#Criando um socket UDP 
print >> sys.stderr, 'Criando um socket UDP'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f.writelines('Socket UDP criado\n')

#conectando o socket a porta em que o servidor esta escutando 
server_address = (sys.argv[1], 10000)
print >>sys.stderr, '\nIniciando em %s porta %s' % server_address
f.writelines('Conexao iniciada\n')

try:
	#Chamando a Camada Fisica
	subprocess.check_output(['./client', sys.argv[1], sys.argv[2]])
	f.writelines('Envio da Camada de Transporte para Fisica efetuado\n')
	print >>sys.stderr, 'Envio da Camada de Transporte para Fisica'

finally:
	print >>sys.stderr, 'Socket fechado'
	f.writelines('Conexao encerrada\n')
