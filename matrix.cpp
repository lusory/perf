#include <iostream>
#include <chrono>

#define n 2048

double A[n][n];
double B[n][n];
double C[n][n];

int main() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A[i][j] = (double) rand() / (double) RAND_MAX;
            B[i][j] = (double) rand() / (double) RAND_MAX;
            C[i][j] = 0;
        }
    }

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    
    double time_spent = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000000000.0;
    std::cout << time_spent << std::endl;
    return 0;
}