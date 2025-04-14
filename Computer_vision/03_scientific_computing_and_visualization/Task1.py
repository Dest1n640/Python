import enum
import numpy as np
import random
import matplotlib.pyplot as plt

# print(np.arange(-5, 5, 1))
# print(np.linspace(-3.14, 3.14, 10))

# print(np.ones((5, 5)))  # А так же есть zero
# print(np.zeros((5, 5)))

# print(np.eye(4))  # Единичная матрица
# print(np.diag(np.arange((5))))
# print(np.meshgrid(range(3), range(3)))

# arr = np.random.randint(0, 20, 20)
# mask = arr % 2 == 0
# print(arr[mask])
# print(mask)

# arr = np.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
# print(np.sum(arr, axis=0))
# print(np.sum(arr, axis=1))
# print(np.sum(arr))

# plt.figure(1)
# plt.subplot(121)
# plt.plot([1, 2, 3])
# plt.subplot(122)
# plt.plot([3, 2, 1])
# plt.show()

# plt.figure()
# plt.plot([-5, -3, 0, 2, 4, 6], [3, 5, 2, 1, 5, 7], "-r^")
# plt.show()

a, b, c = 2, 3, 1
x = np.arange(-10, 10 + 0.2, 0.2)
y = a + b * x + c

ys = []
for i in range(1, 6):
    ys.append(x**i)

plt.figure(figsize=(7.5, 7.5))
plt.subplot(121)
plt.plot(x, y)
plt.grid()
plt.subplot(122)
for i, y in enumerate(ys):
    plt.plot(x, y, label=f"$x ^ {2}$")
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()
plt.plot()
