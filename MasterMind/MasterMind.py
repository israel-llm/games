import random

continuar = 1

while continuar == 1 :
    print("Bienvenido a YouMasterMind")
    print("Elija el modo de dificultad del juego (1=facil , 2=normal, 3=dificil)")
    dificultad = int(input("Digite el numero de dificultad :"))

    if dificultad == 1 :
        c_digitos = 3
    elif dificultad == 2 :
        c_digitos = 4
    elif dificultad == 3 :
        c_digitos = 5

    digitos = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    codigo = ''

    for a in range(c_digitos):
        elegido = random.choice(digitos)
        while elegido in codigo:
            elegido = random.choice(digitos)
        codigo = codigo + elegido

    print("Debes adivinar un codigo de ",c_digitos, " digitos distintos")
    propuesta = input("¿Que codigo propones?")

    intentos=1

    while propuesta != codigo:
        aciertos = 0
        coincidencias = 0
        for i in range(c_digitos):
            if propuesta[i] == codigo[i]:
                aciertos = aciertos +1
            elif propuesta[i] in codigo :
                coincidencias = coincidencias +1

        print("Tu propuesta ", propuesta, " tiene ", aciertos, " aciertos y ", coincidencias, " coincidencias")
        propuesta = input("Propon otra propuesta: ")
        intentos = intentos +1

    print("FELICIDADES! adivinaste el codigo en ", intentos, " intentos")
    continuar = input("Ingrese 1 si desee jugar otra vez o 0 si desea salir: ")
        
