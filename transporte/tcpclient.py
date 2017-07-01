# Camada de Transporte - Cliente

import socket
import sys
import os

LOCALHOST = "localhost"
TRANSPORT_PORT_CLIENT = 31112;
INTERNET_PORT_CLIENT = 21112;
MAX_BUF = 65536;

f = open('clientlogtcp.txt', 'w')
#Criando um socket TCP/IP 
print >> sys.stderr, 'Criando um socket TCP/IP'
appl_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f.writelines('Socket TCP/IP criado\n')

# Vinculando o socket a porta
applayer_address = (LOCALHOST, TRANSPORT_PORT_CLIENT)
print >>sys.stderr, '\nIniciando em %s porta %s' % applayer_address
appl_listener.bind(applayer_address)
# Ouvindo as conexoes recebidas 
appl_listener.listen(5)

while True:
    
    # Esperar por uma conexao
    print >> sys.stderr, '\nAguardando conexao com a Camada de Aplicacao'
    appl_sock, app_address = appl_listener.accept()
    
try:
		#Estabelece conexao com a Camada de Aplicacao		
		print >> sys.stderr, '\nConexao com camada de Aplicacao: ', app_address
		f.writelines('Conexao com camada de Aplicacao estabelecida\n')
		rawdata = appl_sock.recv(MAX_BUF)
		#recv() - recebe os dados a partir da conexao
		origport = os.getpid()
		destport = 8080
		#destport 8080 - comumente usado para proxy web e servidor de armazenamento
		#em cache ou para executar um servidor web como nao root
		data = "Porta origem: " + str(origport) + ", Porta destino: " + str(destport)
		data = data + ',' + 'seq:00, ack:00, data:' + rawdata;
		print >>sys.stderr, 'Data:\n\t"%s"' % data

		netlayer_address = (LOCALHOST, INTERNET_PORT_CLIENT)
		print >>sys.stderr, 'Tentando conectar-se a Camada de Rede em %s porta %s' % netlayer_address
		net_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		net_sock.connect(netlayer_address)
		f.writelines('Conexao com Camada de Rede estabelecida\n')
		print >>sys.stderr, 'Enviando dados para Camada de Rede...'        
		net_sock.sendall(data)
		net_sock.send("\n")
		net_sock.send("")
		sockfd = os.fdopen(net_sock.fileno())
		sockfd.flush()
		f.writelines('Dados enviados a Camada de Rede\n')
        
		# Obtendo resposta da Camada de Rede e enviando de volta 
		# para Camada de Aplicacao
		print >>sys.stderr, 'Dados enviados. Recebendo resposta...'
		data = net_sock.recv(MAX_BUF)
		# AGORA: RECEBE FIN
		# ENVIA ACK

		print >> sys.stderr, '\nResposta:\n%s\n\n' % data
		splitdata = data.split(',')
		data = splitdata[-1]

		print >>sys.stderr, '\nEnviando para Camada de Aplicacao...'
		sent = appl_sock.send(data)
		sent = appl_sock.send("\n")
		sent = appl_sock.send("")
		sockfd = os.fdopen(appl_sock.fileno())
		sockfd.flush()

		# Fechando a conexao
		print >>sys.stderr, '\n\nFechando conexao...\n\n\n'
		net_sock.close()
finally:
	appl_sock.close()
	f.writelines('Conexao fechada\n')



