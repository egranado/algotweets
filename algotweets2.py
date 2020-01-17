import csv
import random
import sys

PATH = 'tweets.csv'
FAVORITOS = 'favoritos.txt'
LARGO_TWEET = 280


def main():
    '''Función principal de la herramienta.'''
    if sys.argv[1] == 'trending':
        if len(sys.argv) < 3:
            print("*Error: Debe ingresar una cantidad.*")
        elif sys.argv[2].isdigit() and sys.argv[2] != '0':
            imprimir_trending(obtener_trending(int(sys.argv[2])))
    if sys.argv[1] == 'favoritos':
        if len(sys.argv) == 2:
            imprimir_favoritos()
        elif sys.argv[2].isdigit():
            imprimir_favoritos(int(sys.argv[2]))
    if sys.argv[1] == 'generar':
        if len(sys.argv) == 2:
            tweet = generar_tweet()
            print(tweet)
            hacer_favorito(tweet)
        elif len(sys.argv) > 2:
            tweet = generar_tweet(sys.argv[2:])
            if not tweet:
                print("*Error: Se ingresó un usuario del cual no se tiene información, intente de nuevo.*")
            else:
                print(tweet)
                hacer_favorito(tweet)


def cargar_datos(path, lista_usuarios=None):
    '''Carga los datos del archivo csv y crea un diccionario con los usuarios como clave y una lista con sus tweets como valor.'''
    tweets_usuario = {}
    try:
        with open(path) as tweets_originales:
            originales_csv = csv.reader(tweets_originales, delimiter='\t')
            for reg in originales_csv:
                if lista_usuarios is None:
                    tweets = tweets_usuario.get(reg[0], [])
                    tweets_usuario[reg[0]] = tweets + [reg[1]]
                elif reg[0] in lista_usuarios:
                    tweets = tweets_usuario.get(reg[0], [])
                    tweets_usuario[reg[0]] = tweets + [reg[1]]
            return tweets_usuario
    except IOError:
        print("Archivo inválido. No puede abrirse.")


def crear_diccionario_markov(lista_usuarios=None):
    '''Guarda en un diccionario todas las palabras de los tweets y las que las suceden, contemplando las repeticiones.'''
    diccionario_markov = {}
    tweets_usuario = cargar_datos(PATH, lista_usuarios)
    if lista_usuarios is None:
        lista_usuarios = list(tweets_usuario)
    for i in range(len(lista_usuarios)):
        if not lista_usuarios[i] in tweets_usuario:
            return {}
            # Devuelve un diccionario vacío si hay por lo menos un usuario del que no hay info
        lista_tweets = tweets_usuario[lista_usuarios[i]]
        for cadena in lista_tweets:
            lista_palabras = cadena.split()
            for i in range(len(lista_palabras)):
                if 0 <= i < len(lista_palabras) - 1:
                    palabras = diccionario_markov.get(lista_palabras[i], [])
                    diccionario_markov[lista_palabras[i]] = palabras + [lista_palabras[i + 1]]
                else:
                    palabras = diccionario_markov.get(lista_palabras[i], [])
                    diccionario_markov[lista_palabras[i]] = palabras + ['']
    return diccionario_markov


def generar_tweet(lista_usuarios=None):
    '''Genera un tweet aleatorio usando cadenas de Markov.'''
    diccionario_markov = crear_diccionario_markov(lista_usuarios)
    if diccionario_markov == {}:
        return False
    claves = list(diccionario_markov)
    palabra_actual = random.choice(claves)
    tweet_aleatorio = palabra_actual
    while True:
        palabra_siguiente = random.choice(diccionario_markov[palabra_actual])
        palabra_actual = palabra_siguiente
        if palabra_siguiente == '':
            return(tweet_aleatorio)
        if len(tweet_aleatorio + " " + palabra_siguiente) > LARGO_TWEET:
            return(tweet_aleatorio)
        tweet_aleatorio += " " + palabra_siguiente


def hacer_favorito(tweet):
    '''Permite elegir si el tweet se guarda como favorito o no.'''
    elegido = input("Ingrese F para guardar el tweet como favorito u otra cosa para descartar: ")
    if elegido.upper() == 'F':
        guardar_favoritos(tweet, FAVORITOS)
        print("Tweet agregado a favoritos.")


def guardar_favoritos(tweet, ruta_destino):
    '''Escribe el tweet en el archivo.'''
    with open(ruta_destino, "a") as favoritos:
        favoritos.write(tweet + "\n")


def imprimir_favoritos(cantidad=None):
    '''Muestra todos los tweets favoritos almacenados, de ingresar una cantidad la muestra en orden cronológico descendente.'''
    try:
        with open(FAVORITOS) as favoritos:
            if cantidad is None:
                for linea in favoritos:
                    print(linea)
            else:
                lista_lineas = list(favoritos)
                if cantidad <= len(lista_lineas):
                    for i in range(cantidad):
                        print(lista_lineas[-1 - i])
                else:
                    print("*Error: la cantidad no puede ser mayor al total de tweets favoritos almacenados.*")
    except IOError:
        print("Archivo inválido. No puede abrirse.")


def obtener_trending(cantidad):
    '''Obtiene los temas más comunes de los que se habla en los tweets almacenados.'''
    lista_hashtags = []
    try:
        with open(PATH) as tweets_originales:
            originales_csv = csv.reader(tweets_originales, delimiter='\t')
            for reg in originales_csv:
                lista_linea = reg[1].split()
                for cadena in lista_linea:
                    if "#" == cadena[0] and cadena not in lista_hashtags:
                        lista_hashtags.append(cadena)
            if cantidad > len(lista_hashtags):
                return lista_hashtags
            return lista_hashtags[:cantidad]
    except IOError:
        print("Archivo inválido. No puede abrirse.")


def imprimir_trending(lista_hashtags):
    '''Imprime los hashtags.'''
    for hashtag in lista_hashtags:
        print(hashtag)


main()