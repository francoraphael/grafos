#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
Programa implementa leitura  de um arquivo contendo 
as informações sobre vértices e arestas de um grafo 
e armazena em um vetor de listas.

Dificuldades
	- Relembrar as nuances de ponteiros em C
	- Ferramenta de debugger
	- Tempo
*/

typedef struct estrutura{
	int info;
	struct estrutura *prox;
}NO;

int input(char str[], int size) {
	int i = 0;
	char c = getchar();
	while (c != '\n') {
		if (size > 0) {
			str[i] = c;
			i++;
			size--;
		}
		c = getchar();
	}
	str[i] = '\0';
	return i;
}

void tokeniza(int *vector, char *token){
	int i = 0;
	while(token != NULL){
		vector[i++] = atoi(token);
		token = strtok(NULL, " ");
	}
}

void insere(NO** grafo, int info, int vertex){
	if(grafo[vertex] == NULL){
		grafo[vertex] = (NO*) malloc(sizeof(NO*));
		grafo[vertex]->info = info;
		grafo[vertex]->prox = NULL;
	}else{
		NO* aux = (NO*) malloc(sizeof(NO*));
		aux->prox = grafo[vertex]->prox;
		aux->info = info;
		grafo[vertex]->prox = aux;
	}
}

void mostra(NO** grafo, int vertex){
	NO *aux = grafo[vertex];
	while(aux != NULL){
		printf("%d\n", aux->info);
		aux = aux->prox;
	}
}

int main(){
	char nomeArquivo[25], buffer[10], *token;
	int i, vector[2], nroVertices;
	FILE *arq;
	NO **grafo;

	printf("Digite o nome do arquivo: ");
	input(nomeArquivo, 25);
	if(!(arq = fopen(nomeArquivo, "r"))){
		printf("A abertura do arquivo FALHOU ! Encerrando o programa !\n");
		exit(1);
	}

	fgets(buffer, sizeof(buffer), arq);
	token = strtok(buffer, " ");
	tokeniza(vector, token);
	nroVertices = vector[0];
	grafo = (NO**) malloc(nroVertices * sizeof(NO*));

	for(i=0; i<nroVertices; i++){
		fgets(buffer, sizeof(buffer), arq);
		token = strtok(buffer, " ");
		tokeniza(vector, token);
		insere(grafo, vector[1], vector[0]);
	}
}