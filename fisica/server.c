/* Referencia antiga: http://www.programminglogic.com/example-of-client-server-program-in-c-using-sockets-and-tcp/ 
   Referência atual:  http://www.binarytides.com/server-client-example-c-sockets-linux/

   Server:
    1. Create socket
	2. Bind to address and port
	3. Put in listening mode
	4. Accept connections and process there after.
*/

#include<stdio.h>
#include<string.h>     /*strlen*/
#include<sys/socket.h>
#include<arpa/inet.h> /*inet_addr*/
#include<unistd.h>    /*write*/
 
int main(int argc, char *argv[]){
    int socket_desc, client_sock, c, read_size;
    struct sockaddr_in server, client;
    char client_message[2000];
     
    /*Create socket*/
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_desc == -1)
      printf("Could not create socket");
    puts("Socket created");
     
    /*Prepare the sockaddr_in structure*/
    server.sin_family      = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port        = htons(8888);
     
    /*Bind*/
    if( bind(socket_desc,(struct sockaddr *)&server, sizeof(server)) < 0){
        perror("bind failed. Error");
        return 1;
    }
    puts("bind done");
     
    /*Listen*/
    listen(socket_desc, 3);
     
    /*Accept and incoming connection*/
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
     
    /* Accept connection from an incoming client*/
    client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
    if (client_sock < 0){
        perror("accept failed");
        return 1;
    }
    puts("Connection accepted");
     
    /*Receive a message from client*/
    while( (read_size = recv(client_sock, client_message, 2000, 0)) > 0 ){
        /*Send the message back to client*/
        write(client_sock ,"Connection made", strlen(client_message));
    }
     
    if(read_size == 0){
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
        perror("recv failed");
     
    return 0;
}
