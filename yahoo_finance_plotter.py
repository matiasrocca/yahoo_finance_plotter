import datetime
from dateutil import tz
import urllib.request
import requests
import json
import sys
import matplotlib.pyplot as plt



############################# FUNCIONES AUXILIARES ############################### 

def quitar_n(l):
    # ".strip" saca del string el elemento que se le pasa. Creamos una nueva lista para ir agregando cada parametro de la busqueda.
    lista_limpia =[]

    for elem in l:
        clean_elem = elem.strip("\n")
        lista_limpia.append(clean_elem)

    return lista_limpia

def lista_parametros(l):
    # Solo iteraremos sobre los dos primeros parametros de la lista original, los correspondientes a las fechas. Devolvemos la lista modificada.
    i = 0
    while i <= 1:
        datetime = to_date(l[i])
        posix = to_posix_timestamp(datetime)
        l[i] = posix
        i += 1

    return l


def get_quote_json(q, init_date, end_date, interval):
    '''Accede a la API de Yahoo! Finance para la accion "q", con la fecha de incio, fin, e intervalo correspondiente
    y devuelve el JSON (dict) correspondiente.'''
    url = "https://query2.finance.yahoo.com/v8/finance/chart/" + q + "?" + "period1="+init_date+"&"+"period2="+end_date+"&"+"interval="+interval+"&"+"events=history"

    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    result = json.loads(r.decode('utf-8')) 

    return result


def func_apertura(q,dict_jsons):
    ret = dict_jsons[str(q)]["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    return ret

def func_cierre(q,dict_jsons):
    ret = dict_jsons[str(q)]["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return ret

def func_rendimientos(q1,q2):
    rendimiento = []
    for apertura, cierre in zip(q1, q2):
        rendimiento.append((cierre-apertura)/apertura)

    return rendimiento

def func_lows(q,dict_jsons):
    ret = dict_jsons[str(q)]["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    return ret

def func_highs(q,dict_jsons):
    ret = dict_jsons[str(q)]["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    return ret

def dias_consecutivos_positivos(l,fechas):
    conteo = 0
    conteo_max = 0
    periodo = [0]*2
    for rendimiento, fecha in zip(l, fechas):
        if rendimiento > 0:
            if conteo == 0:
                inicio_periodo = fecha
            conteo += 1
        else:
            if conteo > conteo_max:
                conteo_max = conteo
                periodo[0] = inicio_periodo
                periodo[1] = fecha
            conteo = 0

    return periodo

def dias_consecutivos_negativos(l,fechas):
    conteo = 0
    conteo_max = 0
    periodo = [0]*2
    for rendimiento, fecha in zip(l, fechas):
        if rendimiento < 0:
            if conteo == 0:
                inicio_periodo = fecha
            conteo += 1
        else:
            if conteo > conteo_max:
                conteo_max = conteo
                periodo[0] = inicio_periodo
                periodo[1] = fecha
            conteo = 0

    return periodo

def diferencia_dias(periodo):
    start_date = datetime.strptime(periodo[0], "%Y/%m/%d")
    end_date =datetime.strptime(periodo[1], "%Y/%m/%d")
    return abs((end_date - start_date).days)

def calculo_de_rendimientos(minimo, maximo):
    ret = (maximo - minimo) / minimo
    return ret

def maximo_rendimiento_obtenible(l, h, fechas):
    
    periodo = [0]*2
    periodo_en_timestamps = [0]*2
    rendimiento_final = -99999999999999999999
    for minimo, date_minimo in zip(l, fechas):
        for maximo, date_maximo in zip(h, fechas):
            rendimiento = calculo_de_rendimientos(minimo, maximo)
            periodo_en_timestamps[0] = to_posix_timestamp(to_date(date_minimo))
            periodo_en_timestamps[1] = to_posix_timestamp(to_date(date_maximo))
            if rendimiento > rendimiento_final and periodo_en_timestamps[0] < periodo_en_timestamps[1]:
                rendimiento_final = rendimiento
                periodo[0] = date_minimo
                periodo[1] = date_maximo

    time_1 = datetime.datetime.strptime(periodo[0], "%Y-%m-%d")
    time_2 = datetime.datetime.strptime(periodo[1], "%Y-%m-%d")

    dias = time_2 - time_1

    periodo = ",".join(periodo)


    return ("Maximo rendimiento = " + str(rendimiento_final) +" Periodo: " + periodo + " " + "Diferencia de dias: " + str(dias))
    
def maximo_rendimiento_obtenible_unittest(l, h, fechas):
    
    periodo = [0]*2
    periodo_en_timestamps = [0]*2
    rendimiento_final = -99999999999999999999
    for minimo, date_minimo in zip(l, fechas):
        for maximo, date_maximo in zip(h, fechas):
            rendimiento = calculo_de_rendimientos(minimo, maximo)
            periodo_en_timestamps[0] = to_posix_timestamp(to_date(date_minimo))
            periodo_en_timestamps[1] = to_posix_timestamp(to_date(date_maximo))
            if rendimiento > rendimiento_final and periodo_en_timestamps[0] < periodo_en_timestamps[1]:
                rendimiento_final = rendimiento
                periodo[0] = date_minimo
                periodo[1] = date_maximo

    return (periodo)


def minimo_rendimiento_obtenible(l, h, fechas):
    periodo = [0]*2
    periodo_en_timestamps = [0]*2
    rendimiento_final = 99999999999
    for minimo, date_minimo in zip(l, fechas):
        for maximo, date_maximo in zip(h, fechas):
            rendimiento = calculo_de_rendimientos(maximo, minimo)
            periodo_en_timestamps[0] = to_posix_timestamp(to_date(date_minimo))
            periodo_en_timestamps[1] = to_posix_timestamp(to_date(date_maximo))
            if rendimiento < rendimiento_final and periodo_en_timestamps[0] > periodo_en_timestamps[1]:
                rendimiento_final = rendimiento
                periodo[1] = date_minimo
                periodo[0] = date_maximo

    time_1 = datetime.datetime.strptime(periodo[0], "%Y-%m-%d")
    time_2 = datetime.datetime.strptime(periodo[1], "%Y-%m-%d")

    dias = time_2 - time_1

    periodo = ",".join(periodo)


    return ("Minimo rendimiento = " + str(rendimiento_final) +" Periodo: " + periodo + " " + "Diferencia de dias: " + str(dias))

def minimo_rendimiento_obtenible_unittest(l, h, fechas):
    periodo = [0]*2
    periodo_en_timestamps = [0]*2
    rendimiento_final = 99999999999
    for minimo, date_minimo in zip(l, fechas):
        for maximo, date_maximo in zip(h, fechas):
            rendimiento = calculo_de_rendimientos(maximo, minimo)
            periodo_en_timestamps[0] = to_posix_timestamp(to_date(date_minimo))
            periodo_en_timestamps[1] = to_posix_timestamp(to_date(date_maximo))
            if rendimiento < rendimiento_final and periodo_en_timestamps[0] > periodo_en_timestamps[1]:
                rendimiento_final = rendimiento
                periodo[1] = date_minimo
                periodo[0] = date_maximo

    return periodo

def to_date(strdate):
    '''toma un string en formato %Y-%m-%d y lo convierte a algo de tipo fecha'''
    return datetime.datetime.strptime(strdate, '%Y-%m-%d')

def to_ymd(ts):
    ''' Toma un timestamp y lo convierte a un string con formato %Y-%m-%d'''
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

def to_posix_timestamp(date):
    '''Toma un datetime y lo convierte a timestamp formato POSIX'''
    return (date - datetime.datetime.utcfromtimestamp(0)).total_seconds() + 14400


############################# FUNCION PRINCIPAL ############################### 
def main():
    ''' Es la funcion principal donde se ejecuta nuestro programa.'''

    # Leemos el archivo input.cfg con los parametros para la ejecucion.
    archivo = open("input.cfg")
    leer_archivo = archivo.readlines()
    lista_limpia = quitar_n(leer_archivo) # Y usamos la función "quitar_n()" para eliminar de los strings el salto de linea al final de cada linea

    archivo.close()

    # Recordar que las fechas estan en formato yyyy-mm-dd
    # Recordar que los posibles valores para el intevalo son los siguientes:
    # ["1d","5d","1wk","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]

    # En la variable parametros guardamos los parametros que recibimos cambiando el formato de las fechas a "timestamps", esto es necesario para el query al solicitar el archivo JSON.
    parametros = lista_parametros(lista_limpia)


    # Obtenemos las fechas de inicio y fin, el intervalo, y las acciones a analizar.
    # Las guardamos en quotes.
    quotes = parametros

    # Separamos los parametros en dos listas distintas, las acciones por un lado y las fechas e intervalo por otro.
    # Para esto iteramos de atras hacia adelante, llegando siempre hasta la posicion numero 2 de la lista de parametros, posicion en la que se encuentra el intervalo. Esto permite
    # que podamos incluir todas las acciones que querramos sin preocuparnos por el funcionamiento del codigo.
    # Eliminamos de la lista original cada accion que sumamos a la lista de acciones.
    lista_acciones = []
    i = len(quotes)-1
    while i > 2:
        lista_acciones.append(quotes[i])
        quotes.pop()
        i -= 1

    # Obtenemos el JSON.
    # El JSON correspondiente a cada accion lo guardamos en un diccionario como significado, como clave guardamos la accion.
    dict_jsons = {}
    for q in lista_acciones:
        dict_jsons[q] = (get_quote_json(q,str(int(quotes[0])),str(int(quotes[1])),quotes[2]))

    # Extraemos y procesamos la informacion.

    # Las fechas seran las mismas para todas las acciones dado que el pedido comparte el periodo, por eso es indiferente que accion usemos para guardarlas.
    fechas = dict_jsons[str(lista_acciones[0])]["chart"]["result"][0]["timestamp"]

    # Calculamos los rendimientos iterando sobre la lista de acciones y los guardamos en una lista de listas, cada posicion en la lista es la lista de rendimientos de una accion. Esa
    # lista de rendimientos son todos los rendimientos diarios para esa accion en ese periodo.
    lista_rendimientos = []
    for q in lista_acciones:
        apertura = func_apertura(q,dict_jsons) # Esta funcion solicita todos los precios de apertura.
        cierre = func_cierre(q,dict_jsons) # Esta funcion solitita todos los precios de cierre
        rendimientos = func_rendimientos(apertura, cierre) # Esta funcion hace el calculo con cada precio de cierre y de apertura diario.
        lista_rendimientos.append(rendimientos)


    # Agregamos el grafico de la serie.
    # Para esto tenemos que volver a transformar el formato de las fechas, de timestamps las pasamos al formato de los strings originales.
    lista_fechas = []
    for date in fechas:
        lista_fechas.append(to_ymd(date))

    # Ploteamos el grafico usando la funcion "plt.plot" para cada lista de rendimientos de la lista que aloja a todas las listas de rendimientos
    for i in range(len(lista_rendimientos)):
        plt.plot(lista_fechas,lista_rendimientos[i],"o-")
        

    # Agregamos la leyenda al grafico.

    plt.legend(lista_acciones)
    
    # Calculamos las metricas. El comentario y explicación a cada paso de esta sección y sus funciones correspondientes se encuentra en el informe correspondiente al último punto del trabajo.

    #Periodo con maxima cantidad de dias consecutivos con rendimiento positivo

    # Agregamos a listas todos los periodos requeridos. Esta lista de periodos queda ordenada al igual que la lista de acciones, lo que nos sirve para despues iterar en conjunto para hacer el diccionario
    # que incluye a la accion y su periodo.

    lista_periodos_positivos = []
    for rendimiento in lista_rendimientos:
        periodo = dias_consecutivos_positivos(rendimiento,lista_fechas)
        lista_periodos_positivos.append(periodo)
    
    diccionario_periodos_positivos = {}

    for accion, periodo in zip(lista_acciones, lista_periodos_positivos):
        diccionario_periodos_positivos[accion] = periodo

    # Periodo con la maxima cantidad de días consecutivos con rendimiento negativo

    lista_periodos_negativos = []
    for rendimiento in lista_rendimientos:
        periodo = dias_consecutivos_negativos(rendimiento,lista_fechas)
        lista_periodos_negativos.append(periodo)

    diccionario_periodos_negativos = {}

    for accion, periodo in zip(lista_acciones, lista_periodos_negativos):
        diccionario_periodos_negativos[accion] = periodo

    print("Periodo con maxima cantidad de dias consecutivos con rendimiento positivo:")
    print(diccionario_periodos_positivos)
    print("Periodo con la maxima cantidad de dias consecutivos con rendimiento negativo:")
    print(diccionario_periodos_negativos)


    # Para el tercer y cuarto punto del ejercicio 5 necesitamos volver a traer del JSON dos listas, esta vez la lista de precios minimos y la lista de precios maximos para cada accion.
    # Para esto, creamos dos listas vacias y las llenamos iterando por accion, llamando a las funciones "func_lows()" y "func_highs()" que se encargan de meterse en el JSON y devolver ese listado.
    # El resultado son dos listas de listas.
    lista_lows = []
    lista_highs = []

    for accion in lista_acciones:
        lista_lows.append(func_lows(accion, dict_jsons))
        lista_highs.append(func_highs(accion, dict_jsons))


    # Maximo y minimo rendimiento obtenible en el periodo
    # Para mostrar los resultado con claridad, decidimos hacer dos diccionarios:
    # uno para los máximos rendimientos, y otro para los mínimos. Para esto iteramos
    # sobre la lista de acciones y la lista de lows y highs de cada una de las acciones
    # y fuimos ingresando lo que definimos en la función al diccionario. 
    maximos_rendimientos = {}
    minimos_rendimientos = {} 
    for accion, lows, highs  in zip(lista_acciones, lista_lows, lista_highs):
        maximos_rendimientos[accion] = maximo_rendimiento_obtenible(lows, highs, lista_fechas)
        minimos_rendimientos[accion] = minimo_rendimiento_obtenible(lows, highs, lista_fechas)


    print(maximos_rendimientos)
    print(minimos_rendimientos)

    # Hacemos show del grafico.

    plt.show()

if __name__ == '__main__':
    main()

