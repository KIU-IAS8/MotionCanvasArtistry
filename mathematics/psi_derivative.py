def psi_derivative(x, epsilon=1e-3):
    """
    Computes the derivative of the function psi(x) = sqrt(x + epsilon)

    Args:
        x (numpy.ndarray or float): Input values
        epsilon (float, optional): A small positive constant for numerical stability

    Returns:
        numpy.ndarray or float: Derivative values of psi(x) with respect to x
    """
    import numpy as np  # You can remove this line if you've already imported NumPy

    if isinstance(x, (int, float)):
        x = np.array([x])

    y = 1.0 / (2 * np.sqrt(x + epsilon))
    return y
