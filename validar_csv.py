#!/usr/bin/python3
#funcion que valida los campos del csv
def validar(nombre_archivo):
    import csv
    class LongitudRegistroIncorrectaError(Exception):
        pass

    class MiError(Exception):
        pass
    CANTIDAD_CAMPOS = 5 #es el valor de las variables que tiene el archivo CSV
    try:
        with open(nombre_archivo, 'r', encoding='latin-1') as archivo:
            print('El archivo se abrió CORRECTAMENTE!!!!!!')
            archivo_csv=csv.reader(archivo)
            registro = 1
            campo = 1
            for linea in archivo_csv:
                if len (linea) != CANTIDAD_CAMPOS:
                    raise LongitudRegistroIncorrectaError()
                else:
                    x=0
                    for x in range(CANTIDAD_CAMPOS):
                        campo = x + 1
                        if linea[x] == '':
                            error= 'El campo {} esta VACÍO en el Registro {}'.format(campo, registro)
                            raise MiError(error)
                        else:
                            pass
                        if registro == 1:
                            detec_colum = linea[x].strip(' ')
                            detec_colum = detec_colum.upper()
                            if detec_colum == 'PRECIO':
                                colum_precio = x
                            elif detec_colum =='CANTIDAD':
                                colum_cantidad = x
                            else:
                                pass
                        else:
                            if x == colum_cantidad:
                                val_columa=int(float(linea[x]))
                            elif x == colum_precio:
                                detec_colum = linea[x].strip(' ')
                                if detec_colum.isdigit() == True:
                                    raise ValueError()
                                else:
                                    f=float(linea[x])
                            else:
                                pass

                registro = registro + 1
            print('ARCHIVO CORRECTO!!!!')
    except FileNotFoundError:
        print('No se encuentra el archivo')
    except PermissionError:
        print('No tenes permisos sobre el archivo')
    except LongitudRegistroIncorrectaError:
        mensaje='{} no tiene los campos correctos'.format(linea)
        print(mensaje)
        with open('Error.log','w') as error_file:
            error_file.write(mensaje)
    except ValueError:
        if x == colum_cantidad:
            print('El Registro {} tiene un Valor Incorrecto en el campo "CANTIDAD'.format(registro))
        else:
            print('El Registro {} tiene un Valor Incorrecto en el campo "PRECIO"'.format(registro, x))







