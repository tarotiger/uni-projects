// Lance-Williams Algorithm for Hierarchical Agglomerative Clustering
// COMP2521 Assignment 2

#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "LanceWilliamsHAC.h"
#include <math.h>

#define INF (0xFFFFFFFF)

// Initialises a dendrogram 
static Dendrogram *newDendrogram(Graph g) {
    Dendrogram *newDend = malloc(GraphNumVertices(g) * sizeof(struct DNode));

    for (int i = 0; i < GraphNumVertices(g); i++) {
        newDend[i] = malloc(sizeof(struct DNode)); 
        newDend[i]->vertex = i; 
        newDend[i]->left = NULL;
        newDend[i]->right = NULL;
    }

    return newDend;
}

// Returns a dendrogram node containing given vertex 
static Dendrogram newDNode(int vertex) {
    Dendrogram newDend = malloc(sizeof(struct DNode));

    // Initialises value of the dendrogram 
    newDend->vertex = vertex; 
    newDend->left = NULL;
    newDend->right = NULL; 

    return newDend;
}

// Returns a two member array which is the column and row 
static int *minDistance(double **dist, int length, int *deleted) {
    double min = INF;
    int *minDist = malloc(2 * sizeof(int)); 
    int row = -1, col = -1; 

    for (int i = 0; i < length; i++) {
        if (deleted[i] == 0) {
            row++;
        } else {
            continue; 
        }
        col = -1; 
        for (int j = 0; j < length; j++) {
            if (deleted[j] == 0) {
                col++; 
            } else {
                continue; 
            }
            if (row == col) {
                continue; 
            }
            if (min >= dist[i][j] && dist[i][j] != -1) {
                min = dist[i][j];
                // Updates the minimum row and column 
                minDist[0] = i;
                minDist[1] = j; 
            }
        }
    }

    // Ensures the first index of minDist is the smaller of the two 
    // vertexes 
    if (minDist[0] > minDist[1]) {
        int temp = minDist[0];
        minDist[0] = minDist[1];
        minDist[1] = temp;
    }

    return minDist;
}

// Removes specified column by converting the column to -1 
static void updateArray(double **dist, int col, int length) {
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length; j++) {
            if (i == col || j == col) {
                dist[i][j] = -1; 
            }   
        } 
    }

    return;
}

static double singleLinkageFormula(double **dist, int i, int j, int k) {
    // printf("where i = %d, j = %d, k = %d\n(0.5)*dist[i][k] + (0.5)*dist[j][k] - (0.5)*abs(dist[i][k] - dist[j][k])\n\t= (0.5) * %lf + (0.5) * %lf - (0.5) * %lf\n\t= %lf\n", i, j, k, dist[i][k], dist[j][k], fabs(dist[i][k] - dist[j][k]), (0.5)*dist[i][k] + (0.5)*dist[j][k] - (0.5)*fabs(dist[i][k] - dist[j][k]));
    return (0.5)*dist[i][k] + (0.5)*dist[j][k] - (0.5)*fabs(dist[i][k] - dist[j][k]);
}

static double completeLinkageFormula(double **dist, int i, int j, int k) {
    return (0.5)*dist[i][k] +(0.5)*dist[j][k] + (0.5)*fabs(dist[i][k] - dist[j][k]);
}

// Initialises an adjacency matrix and converts directed graph to non directed 
static double **newAdjacencyMatrix(Graph g) {
    double **dist = malloc(GraphNumVertices(g) * sizeof(double)); 

    // Sets all the values of the matrix to INF to initialise 
	for (int i = 0; i < GraphNumVertices(g); i++) {
        dist[i] = malloc(GraphNumVertices(g) * sizeof(double));
        for (int j = 0; j < GraphNumVertices(g); j++) {
			dist[i][j] = INF; 
		}
	}

    for (int i = 0; i < GraphNumVertices(g); i++) {
        AdjList adjacent = GraphOutIncident(g, i); 
        dist[i][i] = 0; 
        for (AdjList pivot = adjacent; pivot != NULL; pivot = pivot->next) {
            // Initialises distance between nodes 
            double nodeDist = 1.0/(double)(pivot->weight); 

            // Ensures only the lowest distance between two nodes 
            // are stored regardless of direction 
            if (dist[pivot->v][i] < nodeDist) {
                dist[i][pivot->v] = dist[pivot->v][i];
            } else {
                dist[i][pivot->v] = nodeDist;
                dist[pivot->v][i] = nodeDist; 
            }       
        }
    }

    return dist; 
}

static void printAdjacencyMatrix(double **dist, int length) {
    printf("\t");
    for (int i = 0; i < length; i++) {
        printf("%d\t", i);
    }
    printf("\n");
    int row = 0; 
    for (int i = 0; i < length; i++) {
        printf("%d\t", row);
        row++;
        for (int j = 0; j < length; j++) {
            if (dist[i][j] > 1221225472.00) {
                printf("inf\t");
            } else {
                printf("%.2lf\t", dist[i][j]);
            }  
        }
        printf("\n");
    }
}

static void freeAdjacencyMatrix(double **dist, int length) {
    for (int i = 0; i < length; i++) {
        free(dist[i]); 
    }
    free(dist); 

    return; 
}

/**
 * Generates  a Dendrogram using the Lance-Williams algorithm (discussed
 * in the spec) for the given graph  g  and  the  specified  method  for
 * agglomerative  clustering. The method can be either SINGLE_LINKAGE or
 * COMPLETE_LINKAGE (you only need to implement these two methods).
 * 
 * The function returns a 'Dendrogram' structure.
 */
Dendrogram LanceWilliamsHAC(Graph g, int method) {
    double **dist = newAdjacencyMatrix(g); 

    int length = GraphNumVertices(g);
    Dendrogram *cluster = newDendrogram(g); 
    Dendrogram newCluster = NULL; 
    int *deleted = calloc(GraphNumVertices(g), sizeof(int)); 

    for (int i = 1; i < GraphNumVertices(g); i++) {
        // Returns the two closest clusters as an array
        // where closestCluster[0] is the smaller decimal representation of 
        // the two clusters 
        int *closestCluster = minDistance(dist, length, deleted);
        printAdjacencyMatrix(dist, length); 
        printf("closestClusters are: %d and %d\n", closestCluster[0], closestCluster[1]); 
        
        newCluster = newDNode(closestCluster[0]);
        newCluster->left = cluster[closestCluster[0]];
        newCluster->right = cluster[closestCluster[1]]; 

        // Updates the dendrogram by merging the cluster into 
        // closestCluster[0] 
        cluster[closestCluster[0]] = newCluster;

        if (method == SINGLE_LINKAGE) {
            // Updates the distance using single linkage 
            for (int i = 0; i < length; i++) {
                // Since it merges the cluster into the closestCluster[0] 
                // row of the adjacency matrix, it will not update the distance
                if (i == closestCluster[0] || i == closestCluster[1]) {
                    continue; 
                }
                // Column is removed so it will not update 
                if (dist[closestCluster[0]][i] == -1) {
                    continue; 
                }

                dist[closestCluster[0]][i] = singleLinkageFormula(dist, closestCluster[0], closestCluster[1], i);
                dist[i][closestCluster[0]] = dist[closestCluster[0]][i];
            }
        } else if (method == COMPLETE_LINKAGE) {
            // Updates the distance using complete linkage 
            for (int i = 0; i < length; i++) {
                if (i == closestCluster[0] || i == closestCluster[1]) {
                    continue; 
                }
                if (dist[closestCluster[0]][i] == -1) {
                    continue; 
                }

                dist[closestCluster[0]][i] = completeLinkageFormula(dist, closestCluster[0], closestCluster[1], i);
                dist[i][closestCluster[0]] = dist[closestCluster[0]][i];
            }
        }
        deleted[closestCluster[1]] = 1; 
        // Removes old clusters from the collection 
        updateArray(dist, closestCluster[1], length);
        free(closestCluster);
    }

    freeAdjacencyMatrix(dist, GraphNumVertices(g));
    free(cluster);
    return newCluster;
}

/**
 * Frees all memory associated with the given Dendrogram structure.
 */
void freeDendrogram(Dendrogram d) {
    if (d == NULL) {
        return; 
    }

    freeDendrogram(d->left);
    freeDendrogram(d->right); 

    free(d); 
    return; 
}
