// Centrality Measures ADT implementation
// COMP2521 Assignment 2

#include <stdio.h>
#include <stdlib.h>

#include "CentralityMeasures.h"
#include "Dijkstra.h"
#include "PQ.h"


// initialises the NodeValues struct 
static NodeValues newNodeValues(int numNodes) {
	NodeValues newNvs; 
	newNvs.numNodes = numNodes;
	newNvs.values = calloc(numNodes * sizeof(double), numNodes * sizeof(double));

	return newNvs;
}

////////////////////////////////////////////////////////////////////////////////
//////// CLOSENESS CENTRALITY HELPER FUNCTIONS

// returns the number of nodes reachable by the node denoted in
// dijkstra's path 
static double getReachableNodes(ShortestPaths sps) {
	int num = 0; 

	for (int i = 0; i < sps.numNodes; i++) {
		// if the distance between the src vertex and the 
		// ith vertex is not zero, it is reachable 
		if (sps.dist[i] != 0) {
			num = num + 1; 
		}
	}

	return num; 
}

// returns the result of Wasserman and Faust formula for closeness 
// centrality
static double wassermanFaust(int numNodes, ShortestPaths sps) {
	double pathSum = 0; 
	double reachableNodes = getReachableNodes(sps); 
	for (int i = 0; i < numNodes; i++) {
		pathSum = pathSum + sps.dist[i]; 
	}

	if (pathSum == 0) {
		return 0;
	}

	// (n - 1)/(N - 1) * (n - 1)/(sum of all the path distances)
	return ((reachableNodes)/(numNodes - 1)) * ((reachableNodes/pathSum)); 
}

////////////////////////////////////////////////////////////////////////////////
//////// BETWEENESS CENTRALITY HELPER FUNCTIONS 

// returns true if all the values of an array are not -1 
static bool arrayFilled(int *array, int len) {
	for (int i = 0; i < len; i++) {
		if (array[i] == -1) {
			return false; 
		}
	}

	return true; 
}

// static bool isPred(PredNode *path, Vertex curr) {
// 	PredNode *pivot = path;

// 	while (pivot != NULL) {
// 		if (pivot->v == curr) {
// 			return true;
// 		}
// 		pivot = pivot->next; 
// 	} 

// 	return false; 
// }

// returns the number of predecessors of a given node  
static int numPred(PredNode *pred) {
	int num = 0; 
	PredNode *pivot = pred; 

	while (pivot != NULL) {
		num++;
		pivot = pivot->next;
	}

	return num; 
}

static int *numPaths(PredNode **pred, int numNodes, Vertex src) {
	int *numPath = malloc(numNodes * sizeof(int));
	for (int i = 0; i < numNodes; i++) {
		numPath[i] = -1; 
	} 

	numPath[src] = 1; 

	while (!arrayFilled(numPath, numNodes)) {
		for (int i = 0; i < numNodes; i++) {
			if (i == src) {
				continue;
			}
			// the number of paths 
			if (numPred(pred[i]) == 0) {
				numPath[i] = 0; 
				continue;
			} 

			numPath[i] = -1;

			for (PredNode *pivot = pred[i]; pivot != NULL; pivot = pivot->next) {
				if (numPath[pivot->v] == -1) {
					numPath[i] = -1; 
					break; 
				} else if (numPath[i] == -1) {
					numPath[i] = numPath[pivot->v];
				} else {
					numPath[i] += numPath[pivot->v]; 
				}
			}
		}
	}

	return numPath; 
}

static int *numOccurences(PredNode **pred, int numNodes, int *numPath, Vertex curr) {
	int *occurences = malloc(numNodes * sizeof(int)); 
	
	for (int i = 0; i < numNodes; i++) {
		occurences[i] = -1; 
	} 

	occurences[curr] = numPath[curr]; 

	while (!arrayFilled(occurences, numNodes)) {
		for (int i = 0; i < numNodes; i++) {
			if (i == curr) {
				continue; 
			}

			if (pred[i] == NULL) {
				occurences[i] = 0; 
				continue; 
			} 
			
			occurences[i] = -1;

			for (PredNode *pivot = pred[i]; pivot != NULL; pivot = pivot->next) {
				if (occurences[pivot->v] == -1) {
					occurences[i] = -1; 
					break; 
				} else if (occurences[i] == -1) {
					occurences[i] = occurences[pivot->v];
				} else {
					occurences[i] += occurences[pivot->v]; 
				}
			}
		}
	}

	return occurences; 
}

void printArray(int *array, int len) {
	for (int i = 0; i < len; i++) {
		printf("%d: %d -> ", i, array[i]); 
	}

	printf("END\n");
}

static double betweennessFormula(Graph g, Vertex src, int numNodes) {
	double totalPaths = 0;
	double totalOccurences = 0; 
	double totalBetweenness = 0; 

	for (int i = 0; i < numNodes; i++) {
		if (i != src) {
			ShortestPaths path = dijkstra(g, i);
			int *numPath = numPaths(path.pred, numNodes, i);
			int *occurences = numOccurences(path.pred, numNodes, numPath, src);
			for (int j = 0; j < numNodes; j++) {
				if (j != src && path.dist[j] != 0) {
					totalOccurences = occurences[j];
					totalPaths = numPath[j];
					totalBetweenness += totalOccurences / totalPaths;
					// if (src == 11) {
					// 	printf("%d - %d\n", i, j);
					// 	printf("totalBetweeness: %lf\n", totalBetweenness); 
					// }
					if (i == 27 && j == 0 && src == 11) {
						printf("NPATHS AND NVPATHS: %lf and %lf\n", totalPaths, totalOccurences);
					}
				}
			}
			free(numPath);
			free(occurences);
			freeShortestPaths(path);
		}
	}

	return totalBetweenness; 
} 

NodeValues closenessCentrality(Graph g) {
	NodeValues closeness = newNodeValues(GraphNumVertices(g)); 
	
	for (Vertex src = 0; src < GraphNumVertices(g); src++) {
		ShortestPaths path = dijkstra(g, src); 

		closeness.values[src] = wassermanFaust(GraphNumVertices(g), path); 

		freeShortestPaths(path); 
	}

	return closeness;
}

NodeValues betweennessCentrality(Graph g) {
	NodeValues betweenness = newNodeValues(GraphNumVertices(g));

	for (Vertex src = 0; src < GraphNumVertices(g); src++) {
		ShortestPaths path = dijkstra(g, src); 

		betweenness.values[src] = betweennessFormula(g, src, path.numNodes);

		freeShortestPaths(path); 
	}

	return betweenness;
}

NodeValues betweennessCentralityNormalised(Graph g) {
	NodeValues normBetweenness = newNodeValues(GraphNumVertices(g));

	for (Vertex src = 0; src < GraphNumVertices(g); src++) {
		double numNodes = (double)GraphNumVertices(g);
		ShortestPaths path = dijkstra(g, src); 

		double normalise = 1/((numNodes - 1) * (numNodes - 2));

		normBetweenness.values[src] = normalise * betweennessFormula(g, src, path.numNodes);

		freeShortestPaths(path); 
	}

	return normBetweenness;
}

void showNodeValues(NodeValues nvs) {
	for (int i = 0; i < nvs.numNodes; i++) {
		printf("%d: %f\n", i, nvs.values[i]); 
	}
}

void freeNodeValues(NodeValues nvs) {
	free(nvs.values); 
	return; 
}

