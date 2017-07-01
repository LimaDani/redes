#Camada de Transporte - Servidor

import socket
import sys
import os

LOCALHOST = "localhost"
TRANSPORT_PORT_SERVER = 31111;
TRANSPORT_PORT_CLIENT = 31112;
APPLICATION_PORT_SERVER = 41111;
APPLICATION_PORT_CLIENT = 41112;
MAX_BUF = 65536;

f = open('serverlogtcp.txt', 'w')

#Criando um socket TCP/IP
print >> sys.stderr, 'Criando um socket TCP/IP'
net_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f.writelines('Socket TCP/IP criado\n')

#Vinculando o socket a porta
netlayer_address = (LOCALHOST, TRANSPORT_PORT_SERVER)
print >>sys.stderr, 'Iniciando em %s porta %s' % netlayer_address
net_listener.bind(netlayer_address)
#Ouvindo as conexoes recebidas 
net_listener.listen(1)

while True:
	#Estabelece conexao com a Camada de Rede
	print >> sys.stderr, 'Aguardando conexao com a Camada de Rede'
	net_sock, client_address = net_listener.accept()

	try:
		print >> sys.stderr, 'Conexao com camada de Rede: ', client_address
		f.writelines('Conexao com camada de Rede estabelecida\n')
		data = net_sock.recv(MAX_BUF)
		#recv() - recebe os dados a partir da conexao
		print >>sys.stderr, 'data:\n\t"%s"' % data

		#split() - Separa a string conforme o delimitador ',' ate o final do arquivo
		splitdata = data.split(',')
		data = splitdata[-1]
		
		#portas de origem e destino		
		origport = splitdata[0].split(":")[1]
		destport = splitdata[1].split(":")[1]

		#Estabelecendo conexao com a Camada de aplicacao		
		applayer_address = (LOCALHOST, APPLICATION_PORT_SERVER)
		print >>sys.stderr, 'Tentando conectar-se a Camada de Aplicacao em %s porta %s' % applayer_address
		appl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    #connect() - conecta o socket diretamente ao endereco remoto
		appl_sock.connect(applayer_address)
		f.writelines('Conexao com Camada de Aplicacao estabelecida\n')
		print >>sys.stderr, 'Enviando dados para Camada de Aplicacao...'
		#sendall() - envia os dados atraves do socket    
		appl_sock.sendall(data)
		appl_sock.send("\n")
		appl_sock.send("")
		#fileno() - solicitar permisao de E/S do sistema operacional
		sockfd = os.fdopen(appl_sock.fileno())
		sockfd.flush()
		#Obtendo resposta da Camada de Aplicacao e enviando de volta para Camada de Rede
		print >>sys.stderr, 'Dados enviados. Recebendo resposta...'
		f.writelines('Dados enviados a Camada de Aplicacao\n')
		data = appl_sock.recv(MAX_BUF)
		#recv() - recebe os dados a partir da conexao
		data = "Porta origem: " + str(destport) + ", Porta de destino: " + str(origport) + ',' + data;
		print >> sys.stderr, '\nResposta:\n%s\n\n' % data
		print >>sys.stderr, '\nEnviando para Camada de Rede...'
		sent = net_sock.send(data)
		sent = appl_sock.send("\n")
		sent = appl_sock.send("")
		sockfd = os.fdopen(appl_sock.fileno())
		sockfd.flush()
		f.writelines('Dados enviados a Camada de Rede\n')
		print >>sys.stderr, '\n\nFechando a conexao...\n\n\n'
		appl_sock.close('Conexao com Camada de Aplicacao fechada\n')

	finally:
		net_sock.close()
		f.writelines('Conexao com a Camada de Redes fechada\n')



