#!/usr/bin/python3

#generador de objetos con un registro CSV

import csv
def classificar(nombre_archivo):
    class Csv:#clase de registro del csv
        def __init__ (self, cliente, codigo, producto, cantidad, precio):
            self.cliente = cliente
            self.codigo = codigo
            self.producto = producto
            self.cantidad = cantidad
            self.precio = precio
        def __str__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __repr__ (self):
            return '{}, {}, {}, {}, {}'.format(self.cliente, self.codigo, self.producto, self.cantidad, self.precio)
        def __gt__ (self, otro):
            return self.cantidad > otro.cantidad
        def compra (self):
            return self.cantidad * self.precio

    col_cliente = 0
    col_codigo = 0
    col_producto = 0
    col_cantidad = 0
    col_precio = 0
    col_detec_campo = 0
    registros = []

    with open(nombre_archivo, 'r', encoding = 'latin-1') as archivo:
        archivo_csv = csv.reader(archivo)
        x = 0
        for linea in archivo_csv:
            if x == 0:
                y = 0
                for y in range(5):
                    detec_campo = linea[y].strip(' ')
                    detec_campo = detec_campo.upper()#mayusculeo los campos de la primera linea para poder comparar
                    if detec_campo == 'CLIENTE':
                        col_cliente = y
                    elif detec_campo == 'CODIGO':
                        col_codigo = y
                    elif detec_campo == 'PRODUCTO':
                        col_producto = y
                    elif detec_campo == 'CANTIDAD':
                        col_cantidad = y
                    else:
                        col_precio = y
                    y = y + 1
                x = x + 1
            else:
                registros.append(Csv(cliente = linea[col_cliente].strip(' ').upper(), codigo = linea[col_codigo].strip(' '), producto = linea[col_producto].strip(' ').upper(), cantidad = float(linea[col_cantidad].strip(' ')), precio = float(linea[col_precio].strip(' '))))
    return (registros)