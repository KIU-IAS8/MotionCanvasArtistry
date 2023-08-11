import numpy as np


def split(A, b, w, flag):
    """
    Sets up the matrix splitting for stationary iterative methods: jacobi and sor (gauss-seidel when w = 1.0)

    Args:
        A (numpy.ndarray): Double precision matrix
        b (numpy.ndarray): Double precision right hand side vector (for SOR)
        w (float): Double precision relaxation scalar
        flag (int): Integer flag for method: 1 = jacobi, 2 = sor

    Returns:
        M (numpy.ndarray): Double precision matrix
        N (numpy.ndarray): Double precision matrix such that A = M - N
        b (numpy.ndarray): Double precision rhs vector (altered for SOR)
    """
    m, n = A.shape

    if flag == 1:  # jacobi splitting
        M = np.diag(np.diag(A))
        N = np.diag(np.diag(A)) - A
    elif flag == 2:  # sor/gauss-seidel splitting
        b = w * b
        M = w * np.tril(A, k=-1) + np.diag(np.diag(A))
        N = -w * np.triu(A, k=1) + (1.0 - w) * np.diag(np.diag(A))

    return M, N, b
