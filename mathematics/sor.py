import numpy as np

from mathematics.split import split


def sor(A, x, b, w, max_it, tol):
    """
    sor.m solves the linear system Ax = b using the Successive Over-Relaxation Method
    (Gauss-Seidel method when omega = 1).

    :param A: REAL matrix
    :param x: REAL initial guess vector
    :param b: REAL right hand side vector
    :param w: REAL relaxation scalar
    :param max_it: INTEGER maximum number of iterations
    :param tol: REAL error tolerance

    :return: x: REAL solution vector
             error: REAL error norm
             iter: INTEGER number of iterations performed
             flag: INTEGER: 0 = solution found to tolerance
                            1 = no convergence given max_it
    """
    flag = 0  # initialization
    iter = 0
    bnrm2 = np.linalg.norm(b)
    if bnrm2 == 0.0:
        bnrm2 = 1.0
    r = b - np.dot(A, x)
    error = np.linalg.norm(r) / bnrm2
    if error < tol:
        return x, error, iter, flag
    M, N, b = split(A, b, w, 2)  # matrix splitting
    for iter in range(1, max_it + 1):  # begin iteration
        x_1 = x
        x = np.linalg.solve(M, np.dot(N, x) + b)  # update approximation
        error = np.linalg.norm(x - x_1) / np.linalg.norm(x)  # compute error
        if error <= tol:
            break  # check convergence
    b = b / w  # restore rhs
    r = b - np.dot(A, x)
    if error > tol:
        flag = 1  # no convergence
    return x, error, iter, flag
