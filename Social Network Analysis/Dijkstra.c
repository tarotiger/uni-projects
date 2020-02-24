// Implementation of Dijkstra's algorithm (single source shortest path)

#include <stdio.h>
#include <stdlib.h>

#include "Dijkstra.h"
#include "PQ.h"

// initialises a ShortestPath struct for the algorithm 
// takes in number of nodes and the source vertex 
// typedef struct ShortestPaths {
// 	int numNodes;    // The number of vertices in the graph
	
// 	Vertex src;      // The source vertex
	
// 	int *dist;       // An  array  of distances from the source vertex -
// 	                 // one for each vertex (the distance  from  src  to
// 	                 // itself is 0)
// 	                 // dist[v] contains the distance from src to v
	                 
// 	PredNode **pred; // An  array  of  predecessor  lists - one for each
// 	                 // vertex
// 	                 // pred[v] contains the predecessor list for vertex
// 	                 // v
// } ShortestPaths;
static ShortestPaths newShortestPaths(int numNodes, Vertex src) {
	ShortestPaths path; 

	path.numNodes = numNodes; 
	path.src = src; 

	// allocates memory equal to the number of nodes
	path.dist = malloc(numNodes * sizeof(int));

	// allocates memory for an array of PredNode
	path.pred = malloc(numNodes * sizeof(struct PredNode));

	// intialises all the distances 
	for (int i = 0; i < numNodes; i++) {
		// sets all the distances of the nodes to -1 unless it is 
		// the source node 
		path.dist[i] = (i == src) ? 0 : -1; 
		path.pred[i] = NULL; 
	}

	return path; 
}

// initialises a new PredNode
static PredNode *newPredNode(Vertex v) {
	PredNode *newPred = malloc(sizeof(struct PredNode)); 

	newPred->v = v; 
	newPred->next = NULL;

	return newPred; 
}

// appends value to PredNode 
// adds the predecessor 'src' to the linked list with index 'dest' 
static void appendPredNode(PredNode **list, Vertex dest, Vertex src) {
	PredNode *newPred = newPredNode(src); 

	// predecessor is empty 
	if (list[dest] == NULL) {
		list[dest] = newPred; 
		return; 
	}

	PredNode *pivot = list[dest]; 

	// iterates until one node before NULL node in PredNode 
	while (pivot->next != NULL) {
		pivot = pivot->next; 
	}

	// inserts predNode to end of lsit 
	pivot->next = newPred; 

	return; 
}

// clears the values of the predNode by freeing each node 
static void clearPredNode(PredNode **list, Vertex src) {
	PredNode *pivot = list[src]; 

	// frees each node in the predecessor linked list 
	while (pivot != NULL) {
		PredNode *temp = pivot->next;
		free(pivot);
		pivot = temp; 
	}
	
	list[src] = NULL;
	return; 
}

// initialises a ItemPQ 
// where the key is the vertex and value is the weight 
static ItemPQ newItemPQ(int key, int value) {
	ItemPQ newItem;

	newItem.key = key; 
	newItem.value = value;

	return newItem;  
}

ShortestPaths dijkstra(Graph g, Vertex src) {
	int nV = GraphNumVertices(g); 
	ShortestPaths path = newShortestPaths(nV, src); 

	// intialises an array which indiciates which vertexes have been
	// visited 
	int *visited = malloc(nV * sizeof(int));

	for (int i = 0; i < nV; i++) {
		visited[i] = (i == src) ? 1 : 0; 
	}

	int currWeight = 0; 
	PQ queue = PQNew();
	// adds source vertex of the graph we are traversing to the
	// priority queue 
	PQAdd(queue, newItemPQ(src, 0));

	while (!PQIsEmpty(queue)) {
		// remove the lowest vertex from the queue
		ItemPQ currVertex = PQDequeue(queue); 
		// reset the value of current weight
		currWeight = currVertex.value; 
		// sets the current vertex to visited
		visited[currVertex.key] = 1;

		AdjList neighbours = GraphOutIncident(g, currVertex.key);

		// goes through each unvisited neighbour and adds their 
		// path length to ShortestPaths
		for (AdjList pivot = neighbours; pivot != NULL; pivot = pivot->next) {
			int totalDist = currWeight + pivot->weight; 

			// if the node has been visited then continue to the next node 
			if (visited[pivot->v]) {
				continue;
			}
			
			// no path recorded for the neighbouring nodes 
			if (path.dist[pivot->v] == -1) {
				path.dist[pivot->v] = totalDist; 
				appendPredNode(path.pred, pivot->v, currVertex.key); 
				PQAdd(queue, newItemPQ(pivot->v, totalDist)); 
			// adds a new predecessor to PredNode if weight are the same
			} else if (totalDist == path.dist[pivot->v]) {
				appendPredNode(path.pred, pivot->v, currVertex.key); 
			// new distance is less than the currently recorded distance 
			// so predecessor linked list is cleared and a new predeccesor is 
			// added 
			} else if (totalDist < path.dist[pivot->v]) {
				// printf("THE NODE IS: %d\n", pivot->v);
				path.dist[pivot->v] = totalDist;
				clearPredNode(path.pred, pivot->v); 
				appendPredNode(path.pred, pivot->v, currVertex.key);
				PQUpdate(queue, newItemPQ(pivot->v, totalDist));
			}
		}
	}

	for (int i = 0; i < nV; i++) {
		if (path.dist[i] == -1) {
			path.dist[i] = 0; 
		}
	}

	free(visited); 
	PQFree(queue); 
	return path; 
}

void showShortestPaths(ShortestPaths sps) {
	printf("NUMBER OF NODES: %d\n", sps.numNodes); 
	printf("SOURCE VERTEX: %d\n", sps.src);
	printf("DIST:\n");
	for (int i = 0; i < sps.numNodes; i++) {
		if (i == sps.src) {
			printf("%d: SRC\n", sps.src); 
		} else {
			printf("%d: %d distance\n", i, sps.dist[i]); 
		}
	} 
	printf("PRED:\n"); 
	for (int i = 0; i < sps.numNodes; i++) {
		printf("%d: ", i);
		for (PredNode *pivot = sps.pred[i]; pivot != NULL; pivot = pivot->next) {
			printf("%d -> ", sps.pred[i]->v); 
		}
		printf("X\n"); 
	}
}

void freeShortestPaths(ShortestPaths sps) {
	free(sps.dist);
	for (int i = 0; i < sps.numNodes; i++) {
		clearPredNode(sps.pred, i); 
	} 
	free(sps.pred);

	return; 
}
