#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define FRAME "frame.hex"

void error(char *msg)
{
    perror(msg);
    exit(0);
}

/* Tabela de conversao char -> Hex*/
char c2h[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F'};

/* Criador de colisoes */
int checkColision(){       

    int number = rand() % 100;
    /* Intervalo de colisao */
    if(number >= 10 && number <=30){
        int sleepingTime = rand() % 10;  
        printf("[ INFO ] Colisao detectada. sleep(%d)\n", sleepingTime);
        sleep(sleepingTime);
        /* TODO: Registrar colisao */
        return -1;
    }
    
    return 0;
}

int main(int argc, char *argv[])
{
    int sockfd, port;
    int tmq;
    struct sockaddr_in server;
    struct hostent *hostname;

    /* MAC source */
    char msource[13]; 

    /* MAC destination*/
    char mdest[13];

    int i;
    int length;
    char* message;
 
    FILE* frame;    
    char buffer[256];
    int n;

    if (argc < 4) {
       fprintf(stderr,"[ INFO ] Usage: %s [HOSTNAME] [PORT] \"[MESSAGE]\"\n", argv[0]);
       exit(0);
    }

    /* Tratando parametros */
    hostname = gethostbyname(argv[1]);
    port = atoi(argv[2]);

    length = strlen(argv[3]);
    message = (char*)malloc(sizeof(char)*length*2);
    for(i=0; i<length; i++){
        message[2*i]     = c2h[argv[3][i]/16];
        message[2*i + 1] = c2h[argv[3][i]%16];
    }

    /* Abrindo socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if(sockfd < 0){
        printf("[ ERRO ] %d\n", __LINE__);
        return 1;
    }

    if(hostname == NULL) {
        fprintf(stderr,"[ ERRO ] %d\n", __LINE__);
        exit(0);
    }

    server.sin_family = AF_INET;
    bcopy((char *)hostname->h_addr,
        (char *)&server.sin_addr.s_addr,
        hostname->h_length
    );

    server.sin_port = htons(port);
    if(connect(sockfd,(struct sockaddr *)&server,sizeof(server)) < 0){
        printf("[ ERRO ] %d\n",__LINE__);
    }

    /* TODO: MAC destino e MAC de origem fake */
    strcpy(mdest, "3A971A178FF2");
    strcpy(msource, "E13C86911813");

    /* Escrevendo frame em arquivo */
    frame = fopen(FRAME, "wb+");
    fwrite(msource, sizeof(char), 12, frame);
    fwrite(mdest, sizeof(char), 12, frame);
    fwrite(message, sizeof(char), length*2, frame);
 
    write(sockfd,"TMQ", 3);
    read(sockfd, &tmq, sizeof(int));
    printf("[ INFO ] Solicitado e recebido TMQ: %d\n", tmq);

    /* Enviando frame */
    fseek(frame, 0, SEEK_SET);
    while((n = fread(buffer, sizeof(char), tmq, frame)) > 0){
        while(checkColision() != 0);
        write(sockfd, buffer, sizeof(char)*n);
    }
    free(message);
    fclose(frame);
    /*
    n = write(sockfd,buffer,strlen(buffer));
    if (n < 0) 
         error("ERROR writing to socket");
    bzero(buffer,256);
    n = read(sockfd,buffer,255);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("%s\n",buffer);
    */

    return 0;
}
