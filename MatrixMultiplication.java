import java.util.Random;

public class MatrixMultiplication {
    static final int n = 2048;
    static final double[][] A = new double[n][n];
    static final double[][] B = new double[n][n];
    static final double[][] C = new double[n][n];

    public static void main(String[] args) {
        final Random r = new Random();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                A[i][j] = r.nextDouble();
                B[i][j] = r.nextDouble();
                C[i][j] = 0;
            }
        }

        final long start = System.nanoTime();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        final long stop = System.nanoTime();

        final double timeDiff = (stop - start) * 1e-9;
        System.out.println(timeDiff);
    }
}