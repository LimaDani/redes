# Camada de Transporte - cliente
# Material de consulta Daniele: http://www.clubedohardware.com.br/artigos
# /redes/como-o-protocolo-tcp-ip-funciona-parte-1-r34823/?nbcpage=4

import socket
import sys
import os

LOCALHOST = "127.0.0.1"
TRANSPORT_PORT_CLIENT = 31112;
INTERNET_PORT_CLIENT = 21112;
MAX_BUF = 65536;

# Criando um socket TCP/IP 
appl_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Vinculando o socket a porta
applayer_address = (LOCALHOST, TRANSPORT_PORT_CLIENT)
print >>sys.stderr, 'Iniciando em %s porta %s' % applayer_address
appl_listener.bind(applayer_address)
# Ouvindo as conexoes recebidas 
appl_listener.listen(5)

while True:
    
    # Esperar por uma conexao
    print >> sys.stderr, 'Aguardando conexao com a Camada de Aplicacao'
    appl_sock, app_address = appl_listener.accept()
    
    try:
        # Aceitar conexão de camada de aplicação e solicitação de recebimento
        print >> sys.stderr, 'Conexao com camada de Aplicacao: ', app_address
        rawdata = appl_sock.recv(MAX_BUF)

        
        ### FAZER ALGUM PROCESSAMENTO DE CAMADA DE TRANSPORTE ###
        
        origport = os.getpid()
        destport = 8080
        
        data = "Porta origem:" + str(origport) + ", Porta destino:" + str(destport)
        data = data + ',' + 'seq:00, ack:00, data:' + rawdata;
        print >>sys.stderr, 'Data:\n\t"%s"' % data

        # PRIMEIRO: Envia SYN
        # SEGUNDO: Recebe SYN + ACK
        # TERCEIRO: Envia SYN + package
        # Recebe ACK ...


        # Conexao com a Camada de Internet e envio de dados de solicitação:
        netlayer_address = (LOCALHOST, INTERNET_PORT_CLIENT)
        print >>sys.stderr, 'Tentando conectar-se a Camada de Internet em %s porta %s' % netlayer_address
        net_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        net_sock.connect(netlayer_address)
        print >>sys.stderr, 'Enviando dados para Camada de Internet...'        
        net_sock.sendall(data)
        net_sock.send("\n")
        net_sock.send("")
        sockfd = os.fdopen(net_sock.fileno())
        sockfd.flush()

        
        # Obtendo resposta da Camada de Internet e enviando de volta 
        # para Camada de Aplicacao
        print >>sys.stderr, 'Dados enviados. Recebendo resposta...'
        data = net_sock.recv(MAX_BUF)


        # AGORA: RECEBE FIN
        # ENVIA ACK

        ### FAZER ALGUM PROCESSAMENTO DE CAMADA DE TRANSPORTE ###

        print >> sys.stderr, '\nResposta:\n%s\n\n' % data
        splitdata = data.split(',')
        data = splitdata[-1]

        print >>sys.stderr, 'enviando para Camada de Aplicacao...'
        sent = appl_sock.send(data)
        sent = appl_sock.send("\n")
        sent = appl_sock.send("")
        sockfd = os.fdopen(appl_sock.fileno())
        sockfd.flush()

        # Apenas para fechar a conexão...
        # data = appl_sock.recv(MAX_BUF)
        print >>sys.stderr, '\n\n Fechando conexao...\n\n\n'
        net_sock.close()
    finally:
        # Limpa a conexão
        appl_sock.close()



