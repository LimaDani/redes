#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

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
    
    if (argc < 3){
        fprintf(stderr,"[ INFO ] Usage: %s [PORT] [TMQ]\n", argv[0]);
        exit(1);
    }
    
    /* Criando socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0){
        printf("[ ERRO ] %d\n", __LINE__);
    }

    port = atoi(argv[1]);
    tmq  = atoi(argv[2]);

    server.sin_family      = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port        = htons(port);
    
    if(bind(sockfd, (struct sockaddr *) &server, sizeof(server)) < 0){
        printf("[ ERRO ] %d\n", __LINE__);
    }

    listen(sockfd,5);
    client_l = sizeof(client);
    
    while(1){
        sockfd2 = accept(sockfd, (struct sockaddr *) &client, &client_l);
        if(sockfd2 < 0){
            printf("[ ERRO ] %d\n", __LINE__);
        }
    
        bzero(buffer,256);
        n = read(sockfd2, buffer, 255);
        printf("%d", n);
        if(n < 0){
            printf("[ ERRO ] %d\n", __LINE__);
        }
    
        printf("Here is the message: %s\n",buffer);
        n = write(sockfd2,"I got your message",18);
        if(n < 0){
            printf("[ ERRO ] %d\n", __LINE__);
        }
    }
    return 0; 
}
