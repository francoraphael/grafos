#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct estrutura{
	int info;
	struct estrutura *prox;
}NO;

typedef struct{
	NO *inicio;
}GRAFO;

void inicializar(GRAFO *grafo){
	grafo->inicio = NULL;
}

void mostrar(GRAFO li){
	NO *p = li.inicio;
	printf("\nInicio->[");
	while(p){
		printf("%d", p->info);
		p = p->prox;
		if(p)
			printf(", ");
	}
	printf("]\n");
}

NO* buscaSeq(int info, GRAFO li, NO **ant){
	NO *p = li.inicio;
	*ant = NULL;
	while(p){
		if(p->info == info)
			return p;
		*ant = p;
		p = p->prox;
	}
	return NULL;
}

NO* ultimoElemento(GRAFO li){
	NO *p = li.inicio;
	if(p)
		while(p->prox)
			p = p->prox;
	return p;
}

void inserirNoFim(int info, GRAFO *li){
	NO *novoNo = (NO*)malloc(sizeof(NO));
	NO *ant = ultimoElemento(*li);
	novoNo->info = info;
	novoNo->prox = NULL;
	if(!ant)
		li->inicio = novoNo;
	else{
		ant->prox = novoNo;
	}
}

void inserirNoInicio(int info, GRAFO *li){
	NO *novoNo = (NO*)malloc(sizeof(NO));
	novoNo->info = info;
	novoNo->prox = li->inicio;
	li->inicio = novoNo;
}

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

void alocaGrafo(GRAFO *grafo, int qtdVertices){
	int i = 0;
	grafo = (GRAFO *) malloc(qtdVertices * sizeof(GRAFO));

	for(i = 0; i<qtdVertices; i++)
		inicializar(&grafo[i]);
}

void tokeniza(int *vet, char *token){
	int i = 0;
	while(token != NULL){
		vet[i++] = atoi(token);
		token = strtok(NULL, " ");
	}
}

int main(){
	char nomeArquivo[25], buffer[10], *token;
	int vet[2], i, contador;
	GRAFO *grafo;
	FILE *arq;

	printf("Digite o nome do arquivo: ");
	input(nomeArquivo, 25);
	if(!(arq = fopen(nomeArquivo, "r"))){
		printf("A abertura do arquivo FALHOU ! Encerrando o programa !\n");
		exit(1);
	}

	fgets(buffer, sizeof(buffer), arq);
	token = strtok(buffer, " ");
	tokeniza(vet, token);
	alocaGrafo(grafo, vet[0]);
	contador = vet[1];

	for(i = 0; i<contador; i++){
		fgets(buffer, sizeof(buffer), arq);
		token = strtok(buffer, " ");
		tokeniza(vet, token);
		inserirNoInicio(vet[1], &grafo[vet[0]]);
	}

	mostrar(grafo[4]);

	return 0;
}