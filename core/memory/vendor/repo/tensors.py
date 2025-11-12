# Tensor-scalar encoding placeholder for features/vector
# Converts spectral components and features into a fixed-length numeric vector.
def encode_tensor_scalar(weight: float, G: float, M: float, tokens: int) -> list:
    return [float(weight), float(G), float(M), float(tokens)]
