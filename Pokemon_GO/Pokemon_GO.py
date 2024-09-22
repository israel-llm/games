import random
import sys

# Constantes del juego
MAXP = 13

# Variables Globales
experiencia = 0 
NUMPKB = 20

# Equivalencia de los valores de la matriz
# 0 - 12 = indice de pokemones
# 13 = "*"
# 14 = "J"
# 15 = "W"
# 16 - 20 = "w"

def generaTablero(tablero, pokemones, NUMF, NUMC, NUMPP, NUMPK):

	#Inicializando el tablero vacio
	for f in range(NUMF):
		tablero.append([])
		for c in range(NUMC):
			tablero[f].append(None)

	#Colocar en todo el tablero (*)
	for i in range(NUMF):
		for j in range(NUMC):
			tablero[i][j] = 13

	# Colocamos al jugador en una ubicaion aleatoria del tablero
	posI = random.randrange(0,NUMF)
	posJ = random.randrange(0,NUMC)
	tablero[posI][posJ] = 14

	# Generamos las pokeparadas que seran representadas con 15 en el arreglo bidimensional
	for k in range(NUMPP):
		posI = random.randrange(0,NUMF)
		posJ = random.randrange(0,NUMC)
		if tablero[posI][posJ] == 13 :
			tablero[posI][posJ] = 15
		else:
			k =- 1

	# Generamos los pokemones en el tablero de manera aleatoria
	for z in range(NUMPK):
		posI = random.randrange(0,NUMF)
		posJ = random.randrange(0,NUMC)
		indice = random.randrange(0,MAXP)
		if tablero[posI][posJ] == 13 :
			tablero[posI][posJ] = indice
		else:
			z =- 1


def imprimirTablero(tablero, pokemones, NUMF, NUMC, radJ):
	# Buscamos la posicion del jugador
	for i in range(NUMF):
		for j in range(NUMC):
			if tablero[i][j] == 14 :
				posX = i
				posY = j

	# Imprimir tablero
	for i in range(NUMF):
		for j in range(NUMC):
			# Se mostraran los pokemones al rededor del radio del jugador con un 50% de posibilidad
			if i >= posX - radJ and i <= posX + radJ and j >= posY - radJ and j <= posY + radJ :
				if tablero[i][j] == 14 :
					sys.stdout.write("J ")
				else:
					# Si es que se encuentra una pokeparada en el radio del jugador, se imprime W
					if tablero[i][j] == 15 :
						sys.stdout.write("W ")
					else:
						# Si es que se encuentra una pokeparada girada en el radio del jugador, se imprime w
						if tablero[i][j] >= 16 and tablero[i][j] <= 20 :
							sys.stdout.write("w ")
						else:
							if tablero[i][j] != 13 :
								# 50% de posibilidad de que se muestre el pokemon si esta en el radio del jugador
								mostrar = random.randrange(0,2)
								if mostrar == 1 :
									sentencia = "{} "
									sys.stdout.write(pokemones[tablero[i][j]])
								else:
									sys.stdout.write("* ")
							else:
								sys.stdout.write("* ")
			else:
				# *Ocultar la posicion de los pokemones a la vista pero sí estan en el tablero
				if tablero[i][j] <= 12 and tablero[i][j] >= 0 and tablero[i][j] != 14 :
					sys.stdout.write("* ")
				else:
					# Si es que se encuentra una pokeparada sin girar o girada en el radio del jugador, se imprime W o w
					if tablero[i][j] == 15 :
						sys.stdout.write("W ")
					else:
						if tablero[i][j] >= 16 and tablero[i][j] <= 20 :
							sys.stdout.write("w ")
						else:
							sys.stdout.write("* ")
		print("\n")

def iniciarPokedex(pokedex):
	#Inicializando pokedex vacia
	for i in range(MAXP):
			pokedex.append(None)

def ejecutaComando(tablero, pokemones, pokedex, NUMF, NUMC, comando, radJ) :

	global experiencia
	global NUMPKB
	girado = 0

	if comando == "L" :
		print("Ingrese las coordenadas del pokemon\n")
		fila = int(input("Fila: "))
		columna = int(input("Columna: "))
		print("\n")
		capturarPokemon(tablero, pokemones, pokedex, NUMF, NUMC, fila, columna, radJ);
		
	elif comando == "G" :
		# Buscamos la posicion del jugador para determinar su radio
		for i in range(NUMF) :
			for j in range(NUMC) :
				if tablero[i][j] == 14 :
					posX = i
					posY = j
		
		# Buscamos pokeparadas en el radio del jugador, las cuales estaran definidas con 15 en el arreglo bidimensional
		for i in range(posX - radJ, posX + radJ + 1) :
			for j in range(posY - radJ, posY + radJ + 1) : 
				if tablero[i][j] == 15 :
					experiencia = experiencia + 50
					pokeB = random.randrange(1,5)
					NUMPKB = NUMPKB + pokeB
					# El caracter w es para diferenciar que la pokeparada W fue girada, en el arreglo bi se representara con 16
					tablero[i][j] = 16
					girado = 1
					break

			# Si ya se giro una pokeparada, se considera que no se giran las demas si se encuentran dentro del radio
			if girado == 1 :
				break 
	
	elif comando == "M" :
		direccion = int(input("Ingrese la direccion: "))
		print("\n")
		moverJugador(tablero, NUMF, NUMC, direccion)
	
	else:
		print("El comando ingresado es incorrecto\n")
	
	# Si es que se encuentra una pokeparada girada en el arreglo bi entonces se aumenta en uno para reconocer que ya paso un turno inactivo
	for i in range(NUMF) :
		for j in range(NUMC) :
			if tablero[i][j] >= 16 and tablero[i][j] <= 20 :
				tablero[i][j] = tablero[i][j] + 1
			if tablero[i][j] == 21 :
				tablero[i][j] = 15

def moverJugador(tablero, NUMF, NUMC, direccion) :

	movimientos = 0

	for i in range(NUMF) :
		for j in range(NUMC) :

			if tablero[i][j] == 14 :
				if direccion == 1 :
					if tablero[i][j - 1] == 13 :
						tablero[i][j - 1] = 14  
						tablero[i][j] = 13
					movimientos = 1

				elif direccion == 2 :
					if tablero[i][j + 1] == 13 :
						tablero[i][j + 1] = 14
						tablero[i][j] = 13
					movimientos = 1

				elif direccion == 3 :
					if tablero[i - 1][j] == 13 :
						tablero[i - 1][j] = 14
						tablero[i][j] = 13
					movimientos = 1
				
				elif direccion == 4 :
					if tablero[i + 1][j] == 13 :
						tablero[i + 1][j] = 14
						tablero[i][j] = 13
					movimientos = 1
				
			
			if movimientos == 1 :
				break
		
		if movimientos == 1 :
			break

def capturarPokemon(tablero, pokemones, pokedex, NUMF, NUMC, fila, columna, radJ) :
	
	global experiencia
	global NUMPKB
	# Los datos ingresador por el ususario no consideran las filas y columnas empiezan en 0*
	fila = fila - 1
	columna = columna - 1
	nuevo = 1

	for i in range(NUMF) :
		for j in range(NUMC) :
			if tablero[i][j] == 14 :
				posX = i
				posY = j
	
	# Si el pokemon se encuentra del radio del jugador se evaluará si se atrapa o no
	if fila >= posX - radJ and fila <= posX + radJ and columna >= posY - radJ and columna <= posY + radJ :
		
		# Se analiza si hay un pokemon en la ubicacion ingresada
		if tablero[fila][columna] >= 0 and tablero[fila][columna] <= 12 :
			# 50% de probabilidad de captura
			capturado = random.randrange(0,2)
			NUMPKB -= 1
			if capturado == 1 :
				experiencia = experiencia + 100;
				print("El pokemon ha sido atrapado.\n")
				# Se busca si el pokemon capturado se encuentra en la pokedex del jugador
				# Si el pokemon es nuevo, entonces se registra en el pokedex y se aumenta la exp extra
				indice = tablero[fila][columna]
				if pokemones[indice] != pokedex[indice] :
					pokedex[indice] = pokemones[indice]
					experiencia = experiencia + 100
					print("Pokemon nuevo registrado en Pokedex.\n")
				# Desaparece el pokemon del tablero
				tablero[fila][columna] = 13
			else:
				print("El pokemon no ha sido atrapado.\n")
			
		else:
			# No se encuentra el pokemon en la ubicacion
			print("No hay ningun pokemon en la direccion ingresada\n")

	else:
		print("La direccion ingresada no se encuentra dentro del radio del jugador: \n")


while True:

	tablero = []
	pokemones = ['A', 'B', 'C', 'D', 'E', 'F', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
	pokedex = []
	nivelJ = 1
	fin = 0
	print("Bienvenido a POKE-GO\n")
	nivel = int(input("Ingrese el nivel del juego (1: Principiante, 2: Intermedio, 3: Avanzado): "))
	print("\n")
	if nivel >= 1 and nivel <= 3 :
		if nivel == 1:
			NUMF = 24
			NUMC = 24
			NUMPP = 10
			NUMPK = 10
			radJ = 3
		elif nivel == 2:
			NUMF = 40
			NUMC = 40
			NUMPP = 20
			NUMPK = 60
			radJ = 2
		elif nivel == 3:
			NUMF = 60
			NUMC = 60
			NUMPP = 30
			NUMPK = 120
			radJ = 1

		generaTablero(tablero, pokemones, NUMF, NUMC, NUMPP, NUMPK)
		iniciarPokedex(pokedex)
		expresion = "Nivel del jugador: {}\n"
		print(expresion.format(nivelJ))
		expresion = "Puntos de experiencia: {}\n"
		print(expresion.format(experiencia))
		expresion = "Numero de pokebolas: {}\n"
		print(expresion.format(NUMPKB))
		print("El tablero es el siguiente:\n")
		while fin == 0 :
			imprimirTablero(tablero, pokemones, NUMF, NUMC, radJ)
			comando = input("Ingrese su comando: ")
			print("\n")
			ejecutaComando(tablero, pokemones, pokedex, NUMF, NUMC, comando, radJ)
			if experiencia >= 500 :
				nivelJ += 1
				experiencia = 0
			expresion = "Nivel del jugador: {}\n"
			print(expresion.format(nivelJ))
			expresion = "Puntos de experiencia: {}\n"
			print(expresion.format(experiencia))
			expresion = "Numero de pokebolas: {}\n"
			print(expresion.format(NUMPKB))
			if nivelJ == 5 :
				fin = 1

	else:
		print("Nivel ingresador incorrecto\n")
	
	if fin == 1 : 
		print("Felicidades!!! Eres todo un maestro Pokemon\n")