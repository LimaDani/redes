#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

int checkColiision(){		
    //gera um numero de 0 a 100
    int number = rand() % 100; 
	
    //Faixa de colisao: 10 a 30
    if(number >= 10 && number <=30){
        //Se ocorrer colisao, espera um tempo aleatorio entre 0 e 10s
        int sleepingTime = rand() % 10; 		
        sleep(sleepingTime);
        //registra log da colisao 
        /*A ser implemetado*/

        //retorna valor que indica colisao 
        return -1;
    }
    
    return 0;
}
