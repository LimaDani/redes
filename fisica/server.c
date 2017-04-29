#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

#define OUTPUT "output.data"
#define LOG    "server.log"

void error(char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    int sockfd, sockfd2;
    int port, tmq;
    struct sockaddr_in server, client;
    int client_l;

    char buffer[256];
    int n;

    FILE* output;
    FILE* log;
    
    if (argc < 3){
        fprintf(stderr,"[ INFO ] Usage: %s [PORT] [TMQ]\n", argv[0]);
        exit(1);
    }
    
    /* Abrindo arquivo de LOG */
    log = fopen(LOG, "a");
    fprintf(log, "[ %u ][ INFO ] Iniciou-se o servidor.\n", (unsigned)time(NULL));
    fflush(log);

    /* Criando socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0){
        printf("[ ERRO ] %d\n", __LINE__);
    }

    port = atoi(argv[1]);
    tmq  = atoi(argv[2]);
    fprintf(log, "[ %u ][ INFO ] TMQ estabelecido: %d.\n", (unsigned)time(NULL), tmq);
    fflush(log);

    server.sin_family      = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port        = htons(port);
    
    if(bind(sockfd, (struct sockaddr *) &server, sizeof(server)) < 0){
        printf("[ ERRO ] %d\n", __LINE__);
    }
    
    listen(sockfd,5);
    client_l = sizeof(client);
    
    output = fopen(OUTPUT, "wb");

    while(1){
        sockfd2 = accept(sockfd, (struct sockaddr *) &client, &client_l);
        if(sockfd2 < 0){
            printf("[ ERRO ] %d\n", __LINE__);
        }
 
        fprintf(log, "[ %u ][ INFO ] Conexão estabelecida.\n", (unsigned)time(NULL));
        fflush(log);

        while((n = read(sockfd2, buffer, tmq)) > 0){
            printf("[ INFO ] Lido %d bytes\n", n);
            fprintf(log, "[ %u ][ INFO ] Recebeu quadro de %d bytes.\n", (unsigned)time(NULL), n);
            fflush(log);

            if(strncmp(buffer, "TMQ", 3) == 0){
                write(sockfd2, &tmq, sizeof(int));
                printf("[ INFO ] TMQ (%d) solicitado e enviado. \n", tmq);
                fprintf(log, "[ %u ][ INFO ] Cliente solicitou TMQ.\n", (unsigned)time(NULL));
                fflush(log);
            }else{
                fwrite(buffer, sizeof(char), n, output);
                fflush(output);
                printf("[ INFO ] Salvo no arquivo de output.\n");
                write(sockfd2,"OK", 2);
            }
            bzero(buffer,256);
        }
    }
    return 0; 
}
