import sys
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

def seam_carving(imagen):
    imagen = imread(imagen)
    primer_filtro = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    primer_filtro = np.stack([primer_filtro] * 3, axis=2)

    segundo_filtro = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])

    segundo_filtro = np.stack([segundo_filtro] * 3, axis=2)

    imagen = imagen.astype('float32')
    convolucion = np.absolute(convolve(imagen, primer_filtro)) + np.absolute(convolve(imagen, segundo_filtro))


    mapa_energia = convolucion.sum(axis=2)


    altura, ancho, canales= imagen.shape
    backtracking = np.zeros_like(mapa_energia, dtype=np.int)

    for i in range(1, altura):
        for j in range(0, ancho):
            if j == 0:
                idx = np.argmin(mapa_energia[i - 1, j:j + 2])
                backtracking[i, j] = idx + j
                energia_minima = mapa_energia[i - 1, idx + j]
            else:
                idx = np.argmin(mapa_energia[i - 1, j - 1:j + 2])
                backtracking[i, j] = idx + j - 1
                energia_minima = mapa_energia[i - 1, idx + j - 1]

            mapa_energia[i, j] += energia_minima


    pixeles_a_eliminar = np.ones((altura, ancho), dtype=np.bool)

    elemento_minimo = np.argmin(mapa_energia[-1])

    for i in reversed(range(altura)):
        pixeles_a_eliminar[i, elemento_minimo] = False
        elemento_minimo = backtracking[i, elemento_minimo]

    pixeles_a_eliminar = np.stack([pixeles_a_eliminar] * 3, axis=2)


    imagen = imagen[pixeles_a_eliminar].reshape((altura, ancho - 1, 3))

    return imagen
