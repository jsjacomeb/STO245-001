import numpy as pnum
import imageio
import queue
import pathlib


class Nodo:
	def __init__(self):
		self.probabilidad = None
		self.color = None
		self.izquierda = None
		self.derecha = None
	def __lt__(self, new):
		if (self.probabilidad < new.probabilidad):
			return 1
		else:
			return 0
	def __ge__(self, new):
		if (self.probabilidad > new.probabilidad):
			return 1
		else:
			return 0

def imagenGris(img):
	grey_img = pnum.rint(img[:,:,0]*0.2989 + img[:,:,1]*0.5870 + img[:,:,2]*0.1140)
	grey_img = grey_img.astype(int)
	return grey_img

def arbolProbabilidad(probs):
	colaPrioridad = queue.PriorityQueue()
	for color,probabilidad in enumerate(probs):
		hoja = Nodo()
		hoja.color = color
		hoja.probabilidad = probabilidad
		colaPrioridad.put(hoja)

	while (colaPrioridad.qsize()>1):
		nuevaHoja = Nodo()
		lado_izquierdo = colaPrioridad.get()
		lado_derecho = colaPrioridad.get()

		nuevaHoja.izquierda = lado_izquierdo
		nuevaHoja.derecha = lado_derecho
		nuevaProbabilidad = lado_izquierdo.probabilidad+lado_derecho.probabilidad
		nuevaHoja.probabilidad = nuevaProbabilidad
		colaPrioridad.put(nuevaHoja)
	return colaPrioridad.get()

def construccionHuffman(root_branch,arrayTemporal,texto):
	if (root_branch.izquierda is not None):
		arrayTemporal[construccionHuffman.count] = 1
		construccionHuffman.count+=1
		construccionHuffman(root_branch.izquierda,arrayTemporal,texto)
		construccionHuffman.count-=1
	if (root_branch.derecha is not None):
		arrayTemporal[construccionHuffman.count] = 0
		construccionHuffman.count+=1
		construccionHuffman(root_branch.derecha,arrayTemporal,texto)
		construccionHuffman.count-=1
	else:
		construccionHuffman.output_bits[root_branch.color] = construccionHuffman.count
		codigo_color = ''.join(str(cell) for cell in arrayTemporal[1:construccionHuffman.count])
		color = str(root_branch.color)
		string = color+' '+ codigo_color+'\n'
		texto.write(string)
	return


def Huffman(path):
	for item in pathlib.Path(path).glob('**/*.bmp'):
		img = imageio.imread(item)
		imagen_gris = imagenGris(img)

		histograma = pnum.bincount(imagen_gris.ravel(),minlength=256)
		probabilidad_color = histograma/pnum.sum(histograma)
		raiz = arbolProbabilidad(probabilidad_color)

		arrayTemporal = pnum.ones([64],dtype=int)
		construccionHuffman.output_bits = pnum.empty(256,dtype=int)
		construccionHuffman.count = 0
		texto = open(str(item)+'.txt','w')
		construccionHuffman(raiz,arrayTemporal,texto)

		bits_entrada = img.shape[0]*img.shape[1]*8
		compresion = (1-pnum.sum(construccionHuffman.output_bits*histograma)/bits_entrada)*100
		print('La compresion de la imagen es de',compresion,'%')

Huffman(r"C:\Users\david\OneDrive\Escritorio\Vacas")
