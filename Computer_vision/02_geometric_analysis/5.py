import numpy as np
import matplotlib

a = np.array([1, 2, 3, 4, 5])
print(a)
print(type(a))

print(a.ndim)
print(a.shape)
print(a.size)
print(a.dtype)
print(a.itemsize)

a = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])

print(a.ndim)
print(a.shape)
print(a.size)
print(a.dtype)
print(a.itemsize)
