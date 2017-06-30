#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <ctype.h>

#define FRAME "frame.hex"
#define LOG   "client.log"

#define INTERFACE "/sys/class/net/eth0/address"

/* Tabela de conversao char -> Hex*/
char c2h[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F'};

FILE* log;

/* Criador de colisoes */
int checkColision(){       

    int number = rand() % 100;
    /* Intervalo de colisao */
    if(number >= 10 && number <=30){
        int sleepingTime = rand() % 10;  
        printf("[ INFO ] Colisao detectada. sleep(%d)\n", sleepingTime);
        sleep(sleepingTime);
        
        fprintf(log, "[ %u ][ WARN ] Detectou-se colisão. Dormindo por %d segundos.\n", (unsigned)time(NULL), sleepingTime);
        fflush(log);

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
    char msource[13] = {0}; 

    /* MAC destination*/
    char mdest[13] = {0};

    int i;
    int length;
    char* message;
 
    FILE* frame;    
    char buffer[256];
    int n;
   
    FILE* tmp;
    int j; 
    char t;

    log = fopen(LOG, "a");

    srand(time(NULL));

    if (argc < 4) {
       fprintf(stderr,"[ INFO ] Usage: %s [HOSTNAME] [PORT] \"[MESSAGE]\"\n", argv[0]);
       exit(0);
    }

    /* Tratando parametros */
    hostname = gethostbyname(argv[1]);
    port = atoi(argv[2]);

    fprintf(log, "[ %u ][ INFO ] Procurando se conectar em %s:%d.\n", (unsigned)time(NULL), argv[1], port);
    fflush(log);

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
 
    fprintf(log, "[ %u ][ INFO ] Conexão aberta com sucesso.\n", (unsigned)time(NULL));
    fflush(log);

    /* TODO: MAC destino fake */
    strcpy(mdest, "3A971A178FF2");

    /* Lendo MAC de origem */ 
    tmp = fopen(INTERFACE, "r");
    if(tmp == NULL){
        printf("[ ERRO ] %d\n", __LINE__);
        return 1;
    }
    j = 0;
    while((t = fgetc(tmp))!= EOF && j<12){
        if(t != ':'){
            msource[j++] = toupper(t);
        }
    }
    close(tmp);

    fprintf(log, "[ %u ][ INFO ] MAC de destino identificado: %s. \n", (unsigned)time(NULL), mdest);
    fprintf(log, "[ %u ][ INFO ] MAC de origem identificado: %s. \n", (unsigned)time(NULL), msource);
    fflush(log);

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
        fprintf(log, "[ %u ][ INFO ] Enviando quadro de %d bytes. \n", (unsigned)time(NULL), n);
        fflush(log);
    }
    free(message);
    fclose(frame);
    return 0;
}
