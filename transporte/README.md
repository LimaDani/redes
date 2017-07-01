# Camada de Transportes (Python)

## Server TCP
 1) É criado um socket TCP/IP e vinculado a porta *TRANSPORT_PORT_SERVER*
 2) Uma conexão com a camada de Rede é estabelecida, para tanto, as portas da Camada de Transporte e Camada de Rede, 
    respectivamente, devem ser correspondentes, *TRANSPORT_PORT* = *TRANSPORT_PORT_SERVER*. 
 3) Uma conexão com a camada de Aplicação é estabelecida, para tanto, a porta *APPLICATION_PORT_SERVER*, tanto do lado da Camada de 
    Transporte e Camada de Aplicação (servidor), devem ser correspondentes
 4) Envia dados para a Camada de Aplicação através do socket
 5) Obtém resposta da Camada de Aplicação e envia de volta para Camada de Rede
 6) Fecha a conexão
 7) Para as ações de envio de dados, estabelecimento e fechamento de conexão, são gerados logs no arquivo *serverlogtcp.txt*
 
##### Compilação
- Arquivo: *tcpserver.py*
- $ python tcpserver.py

## Client TCP
 1) É criado um socket TCP/IP e vinculado a porta *TRANSPORT_PORT_CLIENT* 
 2) Uma conexão com a camada de Aplicação é estabelecida, para tanto, a porta *APPLICATION_PORT_CLIENT*, tanto do lado da Camada de 
    Transporte e Camada de Aplicação (servidor), devem ser correspondentes
 3) Recebe dados da a Camada de Aplicação através do socket, organizando o segmento de forma a seguir o padrão especificado para o TCP
 4) Envia dados para a Camada de Rede através do socket
 4) Obtém resposta da Camada de Rede e envia de volta para Camada de Aplicação
 6) Fecha a conexão
 7) Para as ações de envio de dados, estabelecimento e fechamento de conexão, são gerados logs no arquivo *clientlogtcp.txt*
 
##### Compilação
- Arquivo: tcpclient.py
- $ python tcpclient.py

## Server UDP
##### Compilação
- Arquivo: udpserver.py
- $ python udpserver.py

## Client UDP
##### Compilação
- Arquivo: udpclient.py
- $ python udpclient.py



