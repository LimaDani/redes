# Camada de Transporte - Servidor

import socket
import sys
import os

LOCALHOST = "127.0.0.1"
TRANSPORT_PORT_SERVER = 31111;
TRANSPORT_PORT_CLIENT = 31112;
APPLICATION_PORT_SERVER = 41111;
APPLICATION_PORT_CLIENT = 41112;
MAX_BUF = 65536;

# Criando um socket TCP/IP
net_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Vinculando o socket a porta
netlayer_address = (LOCALHOST, TRANSPORT_PORT_SERVER)
print >>sys.stderr, 'Iniciando em %s porta %s' % netlayer_address
net_listener.bind(netlayer_address)
# Ouvindo as conexoes recebidas 
net_listener.listen(1)

while True:
    
    # Esperar por uma conexao
    print >> sys.stderr, 'Aguardando conexao com a Camada de Internet'
    net_sock, client_address = net_listener.accept()
	
    try:
        # Aceitar conexão de Camada de Internet e solicitação de recebimento
        print >> sys.stderr, 'Conexao com camada de Internet: ', client_address
        data = net_sock.recv(MAX_BUF)
        print >>sys.stderr, 'data:\n\t"%s"' % data

        ### FAZER ALGUM PROCESSAMENTO DE CAMADA DE TRANSPORTE ###

        splitdata = data.split(',')
        data = splitdata[-1]
        origport = splitdata[0].split(":")[1]
        destport = splitdata[1].split(":")[1]


        # Conexao com a Camada de Internet e envio de dados de solicitação:
        applayer_address = (LOCALHOST, APPLICATION_PORT_SERVER)
        print >>sys.stderr, 'Tentando conectar-se a Camada de Aplicacao em %s porta %s' % applayer_address
        appl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        appl_sock.connect(applayer_address)
        print >>sys.stderr, 'Enviando dados para Camada de Aplicacao...'      
        appl_sock.sendall(data)
        appl_sock.send("\n")
        appl_sock.send("")
        sockfd = os.fdopen(appl_sock.fileno())
        sockfd.flush()

        
        # Obtendo resposta da Camada de Aplicacao e enviando de volta 
        # para Camada de Internet
        print >>sys.stderr, 'Dados enviados. Recebendo resposta...'
        data = appl_sock.recv(MAX_BUF)

        ### FAZER ALGUM PROCESSAMENTO DE CAMADA DE TRANSPORTE ###

        data = "Porta origem: " + str(destport) + ", Porta de destino: " + str(origport) + ',' + data;

        print >> sys.stderr, '\nResposta:\n%s\n\n' % data
        print >>sys.stderr, 'enviando para Camada de Internet...'
        sent = net_sock.send(data)
        sent = appl_sock.send("\n")
        sent = appl_sock.send("")
        sockfd = os.fdopen(appl_sock.fileno())
        sockfd.flush()

        # Fechando a conexao
        print >>sys.stderr, '\n\nFechando conexao...\n\n\n'
        appl_sock.close()

    finally:
        # Limpa a conexão
        net_sock.close()


