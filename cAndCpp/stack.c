//stack data-structre
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int val;
    struct Node *next;
}Node ;


typedef struct Stack
{
    Node* head;
    int sp;

    
}Stack ;


int main(){
    Node* node1 = ( Node*)malloc(sizeof(Node));
    Node* node2 = ( Node*)malloc(sizeof(Node));
    node1->val = 5;
    node1->next = node2;
    node2->val = 20;
    node2->next = NULL;

    Node* temp = node1;
    while (temp){
        printf("%d\n", temp-> val);
        temp = temp -> next;
    }

    return 0;
}
