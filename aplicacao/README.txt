EXPLICAÇÃO DA CAMADA DE APLICAÇÃO


1) O server.rb deve ser rodado, no terminal, no diretorio da aplicação, com:

ruby server.rb


2) Ao entrar no brownser com o entereço http://localhost:2345 deve haver uma 
resposta de GET no terminal 


3) Para ver as mensagens transmitidas para o servidor do tipo 200 para um 
arquivo presente no diretório /public,  digite num terminal no mesmo caminho 
do diretório: 

curl --verbose -XGET http://localhost:2345/hello.txt, por exemplo. 

O arquivo hello.txt está presente no diretório. 

< HTTP/1.1 200 OK
< Content-Type: text/plain
< Content-Length: 4
< Connection: close


4) Caso você, como cliente, tente acessar o brownser com um nome de arquivo ausente
no diretório public, ocorrerá um erro de "File not found" na página e mensagem 

< HTTP/1.1 404 Not Found
< Content-Type: text/plain
< Content-Length: 15
< Connection: close

no verbose. 




--Fonte principal do corpo do server.rb 

http://practicingruby.com/articles/implementing-an-http-file-server

--Fonte o setting paths 

http://stackoverflow.com/questions/2437390/serving-static-files-with-sinatra
