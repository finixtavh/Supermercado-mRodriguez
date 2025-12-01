import csv
import os
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Manuel Rodriguez || 3D || 17/11
def productoMasCaro(productos) -> str:
    """
    Recibe el objeto del archivo con los productos y devuelve
    el nombre del producto mas caro.
    """
    max_precio = 0
    nombre_producto = ""

    for linea in productos:
        # Separar los datos por comas
        datos = linea.strip().split(',')
        # Separar datos y colocarlos en variables
        id = datos[0]
        nombre = datos[1]
        precio = int(datos[2])
        stock = int(datos[3])

        # Verificar si este producto es más caro
        if precio > max_precio:
            max_precio = precio
            nombre_producto = nombre

    with open('prod.txt', 'w') as informe:
        informe.write(f"{nombre_producto}\n")
    return nombre_producto


# Se abre el archivo y se llama a la función que crearon
with open('productos.csv', 'r') as productos:
  print(f"El producto más caro es: {productoMasCaro(productos)}")

# Manuel Rodriguez || 3D || 17/11
def valorTotalBodega(productos) -> str:
    """
    Recibe el objeto del archivo con los productos y devuelve
    el valor total de lo que se encuentra en bodega.
    Se calcula como: precio * stock de cada producto
    """
    valor_total = 0

    for linea in productos:
        # Separar los datos por comas
        datos = linea.strip().split(',')
        # Separar datos y colocarlos en variables
        id = datos[0]
        nombre = datos[1]
        precio = int(datos[2])
        stock = int(datos[3])

        # Calcular el valor de este producto en bodega
        valor_producto = precio * stock
        valor_total += valor_producto
    with open('value.txt', 'w') as informe:
        informe.write(f"{valor_total}\n")
    return valor_total

# Manuel Rodriguez || 3D || 17/11
def productoConMasIngresos(items, productos):
    """
    Recibe los objetos de los archivos de items y productos y devuelve
    el nombre del producto con más ingresos.
    Los ingresos se calculan como: precio * cantidad vendida
    """
    # Primero, crear un diccionario con los productos (id -> [nombre, precio])
    dict_productos = {}
    for linea in productos:
        datos = linea.strip().split(',')
        id = datos[0]
        nombre = datos[1]
        precio = int(datos[2])
        dict_productos[id] = [nombre, precio]

    # Ahora calcular los ingresos por producto
    ingresos_por_producto = {}

    for linea in items:
        datos = linea.strip().split(';')
        # poner valores como variablkes
        id_venta = datos[0]
        codigo_producto = datos[1]
        cantidad = int(datos[2])

        # Obtener el precio del producto
        if codigo_producto in dict_productos:
            nombre = dict_productos[codigo_producto][0]
            precio = dict_productos[codigo_producto][1]

            # Calcular ingresos de esta venta
            ingreso = precio * cantidad

            # Acumular los ingresos por producto
            if codigo_producto not in ingresos_por_producto:
                ingresos_por_producto[codigo_producto] = {
                    'nombre': nombre,
                    'total': 0
                }
            ingresos_por_producto[codigo_producto]['total'] += ingreso

    # Encontrar el producto con más ingresos
    max_ingresos = 0
    nombre_producto = ""
    # se convierten las claves:valor de ingresos_por_producto a codigo y datos.
    # si datos es menor que max_ingresos: max_ingresos se convierte al valor de
    # datos y nombre producto se convierte al nombre de datos
    for id, datos in ingresos_por_producto.items():
        if datos['total'] > max_ingresos:
            max_ingresos = datos['total']
            nombre_producto = datos['nombre']
    with open('proding.txt', 'w') as informe:
        informe.write(f"{nombre_producto}\n")
    return nombre_producto

with open('productos.csv', 'r') as productos:
  with open('items.csv', 'r') as items:
    print(f"{productoConMasIngresos(items, productos)}")



def totalVentasDelMes(año, mes, items, productos, ventas):
    # Volver al inicio de cada archivo
    productos.seek(0)
    ventas.seek(0)
    items.seek(0)

    # Cargar productos {id: precio}
    productos_dict = {}
    reader = csv.DictReader(productos, delimiter=';')
    for row in reader:
        if row.get('id'):  # Saltar líneas vacías
            productos_dict[row['id']] = int(row['precio'])

    # Cargar ventas {num_boleta: fecha}
    ventas_dict = {}
    reader = csv.DictReader(ventas, delimiter=';')
    for row in reader:
        if row.get('num_boleta'):  # Saltar líneas vacías
            fecha_dt = datetime.strptime(row['fecha'], "%d/%m/%Y")
            ventas_dict[row['num_boleta']] = fecha_dt

    # Calcular total del mes
    total = 0
    reader = csv.DictReader(items, delimiter=';')
    for row in reader:
        if row.get('num_boleta'):  # Saltar líneas vacías
            num_boleta = row['num_boleta']
            if num_boleta in ventas_dict:
                fecha = ventas_dict[num_boleta]
                if fecha.year == año and fecha.month == mes:
                    precio = productos_dict[row['id_producto']]
                    cantidad = int(row['cantidad'])
                    total += precio * cantidad
    with open('total.txt', 'w') as informe:
        informe.write(f"{total}\n")
    return total

# Uso
with open('productos.csv', 'r') as productos, \
     open('items.csv', 'r') as items, \
     open('ventas.csv', 'r') as ventas:
    resultado = totalVentasDelMes(2010, 10, items, productos, ventas)
    print(f"El total de ventas para 10/2010 es: {resultado}")

# Manuel Rodriguez || 3D || 17/11
def productoMasCaro(productos):
    # Volver al inicio del archivo para poder leerlo desde el principio
    productos.seek(0)
    # Crear lector CSV que separa columnas con coma
    reader = csv.reader(productos, delimiter=',')


    max_precio = 0
    nombre_mas_caro = ""

    # Recorrer cada línea del archivo productos.csv
    for row in reader:
        # Verificar que la línea tenga al menos 4 columnas (id, nombre, precio, cantidad)
        if len(row) >= 4:
            # row[1] es la columna del nombre
            nombre = row[1]
            # row[2] es la columna del precio, convertir a número entero
            precio = int(row[2])
            # Si este precio es mayor al máximo encontrado hasta ahora
            if precio > max_precio:
                # Actualizar el precio máximo
                max_precio = precio
                # Guardar el nombre de este producto
                nombre_mas_caro = nombre
    return nombre_mas_caro

def valorTotalBodega(productos):
    # Volver al inicio del archivo
    productos.seek(0)
    # Crear lector CSV con delimitador coma
    reader = csv.reader(productos, delimiter=',')


    total = 0
    for row in reader:
        if len(row) >= 4:
            precio = int(row[2])
            cantidad = int(row[3])
            total += precio * cantidad

    return total

def productoMasVendido(items, productos):
    # Volver al inicio de ambos archivos
    productos.seek(0)
    items.seek(0)


    nombres = {}
    reader = csv.reader(productos, delimiter=',')
    for row in reader:
        if len(row) >= 4:
            nombres[row[0]] = row[1]

    # Diccionario para contar {id_producto: cantidad_total_vendida}
    ventas_por_producto = {}
    # Leer archivo items (delimitador: punto y coma)
    reader = csv.reader(items, delimiter=';')
    for row in reader:
        if len(row) >= 3:
            id_producto = row[1]
            cantidad = int(row[2])
            # Sumar la cantidad al total de este producto
            # .get(id_producto, 0) devuelve 0 si el producto no existe aún en el diccionario
            ventas_por_producto[id_producto] = ventas_por_producto.get(id_producto, 0) + cantidad

    # Encontrar el id del producto con mayor cantidad vendida
    # max() busca la clave (id) con el valor más alto
    id_mas_vendido = max(ventas_por_producto, key=ventas_por_producto.get)
    return nombres[id_mas_vendido]

def totalVentasDelMes(año, mes, items, productos, ventas):
    productos.seek(0)
    ventas.seek(0)
    items.seek(0)

    productos_dict = {}
    # Leer archivo productos
    reader = csv.reader(productos, delimiter=',')
    for row in reader:
        if len(row) >= 4:
            # row[0] es el id, row[2] es el precio
            # Guardar: productos_dict[id] = precio
            productos_dict[row[0]] = int(row[2])


    ventas_dict = {}
    reader = csv.reader(ventas, delimiter=';')
    for row in reader:
        if len(row) >= 3:
            # row[1] contiene la fecha en formato "12-9-2010"
            # strptime convierte el texto a un objeto fecha
            fecha_dt = datetime.strptime(row[1], "%d-%m-%Y")
            # row[0] es el número de boleta
            # Guardar: ventas_dict[num_boleta] = fecha
            ventas_dict[row[0]] = fecha_dt


    total = 0

    reader = csv.reader(items, delimiter=';')
    for row in reader:
        if len(row) >= 3:

            num_boleta = row[0]
            if num_boleta in ventas_dict:
                # Obtener la fecha de esta venta
                fecha = ventas_dict[num_boleta]
                # Verificar si la venta es del año y mes solicitados
                if fecha.year == año and fecha.month == mes:
                    # row[1] es el id del producto, row[2] es la cantidad
                    # Calcular: precio × cantidad y sumarlo al total
                    total += productos_dict[row[1]] * int(row[2])

    return total

# Abrir los tres archivos CSV en modo lectura ('r')
# El 'with' asegura que los archivos se cierren automáticamente al terminar
with open('productos.csv', 'r') as productos, \
     open('items.csv', 'r') as items, \
     open('ventas.csv', 'r') as ventas:

    # Llamar a cada función para obtener la información necesaria
    mas_caro = productoMasCaro(productos)
    valor_bodega = valorTotalBodega(productos)
    mas_vendido = productoMasVendido(items, productos)
    total_mes = totalVentasDelMes(2010, 10, items, productos, ventas)

    with open('informe.txt', 'w') as informe:
        informe.write(f" El producto más caro es {mas_caro}\n")
        informe.write(f" El valor total de la bodega es de ${valor_bodega}\n")
        informe.write(f" El producto con más ingresos es {mas_vendido}\n")
        informe.write(f" En el período de 10/2010, el total de ventas es de ${total_mes}\n")

    with open('informe.txt', 'r') as informe:
        print("\nContenido del informe:")
        # Leer todo el contenido del archivo y mostrarlo
        print(informe.read())