#!/usr/bin/env python
import csv
import validar_csv #modulo de validacion de csv
import class_csv #modulo que me genera una lista de objetos con cada registro
import func_listar #funciones para procesar las busqueda de los listados

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from forms import LoginForm, ProductoForm, ClienteForm

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

#--------------------PROCESOS CON EL ARCHIVO CSV---------------------
nombre_de_archivo = 'farmacia.csv' #se define que archivo 'CSV' voy a abrir
validar_csv.validar(nombre_de_archivo)
registros = class_csv.classificar(nombre_de_archivo)

#-----------------------CONFIGURACIONES------------------------------------------------------
app.config['SECRET_KEY'] = 'una llave que nadie sepa'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

#--------------------ERRORES-------------------------------------------------
@app.errorhandler(404)
def no_encontrado(e):
    if 'username' in session:
        return render_template('Error_404.html'), 404
    else:
        flash('404 - Recurso no encontrado')
        return redirect(url_for('ingresar'))

@app.errorhandler(500)
def error_interno(e):
    if 'username' in session:
        return render_template('Error_500.html'), 500
    else:
        flash('500 - Error en el Servidor')
        return redirect(url_for('ingresar'))

#--------------------------MENUES--------------------
#--------------------------INDEX---------------------
@app.route('/')
def index():
    return render_template('index.html')

#--------------FARMASOFT-----------------------------
@app.route('/farmasoft')
def index2():
    if 'username' in session:
        return render_template('index1.html')
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#--------------INGRESAR------------------------------
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                    flash('Bienvenido '+ formulario.usuario.data)
                    session['username'] = formulario.usuario.data
                    return redirect(url_for('ultimas'))
                registro = next(archivo_csv, None)
            else:
                flash('Id y/o Contraseña invalido/s')
                return redirect(url_for('ingresar'))
    return render_template('login.html', formulario=formulario)

#--------------LOGOUT--------------------

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

#--------------ULTIMAS VENTAS------------------------

@app.route('/ultimas', methods=['GET', 'POST'])
def ultimas():
    if 'username' in session:
        ultimos = 10#se define la variable con la cantidad max de registros que queremos ver
        ul_ventas = []
#        registros = class_csv.classificar(nombre_de_archivo)
        ul_ventas=func_listar.listar_ventas(registros, ultimos)
        return render_template('ultimas.html',ul_ventas=ul_ventas)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#--------------PRODUCTOS COMPRADOS POR CLIENTES----------

@app.route('/prod_clientes', methods=['GET', 'POST'])
def prod_clientes():
    if 'username' in session:
#        registros = class_csv.classificar(nombre_de_archivo)
        formulario = ClienteForm()
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:#advierte que debe ingresar mas de 3 caracteres
                flash('Debe Ingresar por lo menos 3 Caracteres a Buscar')
                return render_template('prod_clientes.html', form = formulario)
            else:
                val = func_listar.encontrar_clientes(registros,cliente)#llama a funcion para validar si exiten los clientes
                if len(val) == 0:
                    flash('No se Encontraron resultados Para su Busqueda')
                elif len(val) == 1:
                    listar = func_listar.listar_productos_cliente(registros,cliente)
                    return render_template('prod_clientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se Encontraron Varios Clientes, Por Favor Seleccione el que Desea Listar')
                    return render_template('prod_clientes.html', form = formulario, clientes = val)
        return render_template('prod_clientes.html', form = formulario)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#--------------Clientes Multiples------------------------

@app.route('/prod_clientes/<clientes>', methods=['GET', 'POST'])
def prod_clientes2(clientes):
    if 'username' in session:
        formulario = ClienteForm()
#        registros = class_csv.classificar(nombre_de_archivo)
        if formulario.validate_on_submit():
            cliente = formulario.cliente.data.upper()
            if len(cliente) < 3:
                flash('Debe Ingresar por lo menos 3 Caracteres a Buscar')
                return redirect(url_for('prod_clientes'))
            else:
                val = func_listar.encontrar_clientes(registros,cliente)
                if len(val) == 0:
                    flash('No se Encontraron resultados Para su Busqueda')
                    return redirect(url_for('prod_clientes'))
                elif len(val) == 1:
                    listar = func_listar.listar_productos_cliente(registros,cliente)
                    return render_template('prod_clientes.html', form = formulario, listar = listar, cliente= formulario.cliente.data.upper())
                else:
                    flash('Se Encontraron Varios Clientes, Por Favor Seleccione el que Desea Listar')
                    return render_template('prod_clientes.html', form = formulario, clientes = val)
        else:
            cliente = clientes
            val = func_listar.encontrar_clientes(registros,cliente)
            listar = func_listar.listar_productos_cliente(registros,cliente)
            return render_template('prod_clientes.html', form = formulario, listar = listar, cliente= cliente)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#--------------CLIENTES QUE COMPRARON UN PRODUCTO--------

@app.route('/clientes_prod', methods=['GET', 'POST'])
def clientes_prod():
    if 'username' in session:
#        registros = class_csv.classificar(nombre_de_archivo)
        formulario = ProductoForm()
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:#validacionde caracteres minimos en la entrada
                flash('Debe Ingresar por lo menos 3 Caracteres a Buscar')
                return render_template('clientes_prod.html', form=formulario)
            else:
                val = func_listar.encontrar_productos(registros, producto)
                if len(val) == 0:
                    flash('No se Encontraron resultados Para su Busqueda')
                elif len(val) == 1:
                    listar = func_listar.listar_clientes_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Se Encontraron Varios productos, Por Favor Seleccione el que Desea Listar')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        return render_template('clientes_prod.html', form=formulario)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#        Productos Multiples-------------------------


@app.route('/clientes_prod/<productos>', methods=['GET', 'POST'])
def cliente_prod2(productos):
    if 'username' in session:
        formulario = ProductoForm()
#        registros = class_csv.classificar(nombre_de_archivo)
        if formulario.validate_on_submit():
            producto = formulario.producto.data.upper()
            if len(producto) < 3:
                flash('Debe Ingresar por lo menos 3 Caracteres a Buscar')
                return redirect(url_for('clientes_prod'))
            else:
                val = func_listar.encontrar_productos(registros,producto)
                if len(val) == 0:
                    flash('No se Encontraron resultados Para su Busqueda')
                    return redirect(url_for('clientes_prod'))
                elif len(val) == 1:
                    listar = func_listar.listar_clientes_producto(registros,producto)
                    return render_template('clientes_prod.html', form = formulario, listar = listar, producto= formulario.producto.data.upper())
                else:
                    flash('Se Encontraron Varios Productos, Por Favor Seleccione el que Desea Listar')
                    return render_template('clientes_prod.html', form = formulario, productos = val)
        else:
            producto = productos
            val = func_listar.encontrar_productos(registros,producto)
            listar = func_listar.listar_clientes_producto(registros,producto)
            return render_template('clientes_prod.html', form = formulario, listar = listar, producto = producto)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))


#--------------PRODUCTOS VENDIDOS--------------------

@app.route('/prod_vendidos', methods=['GET', 'POST'])
def prod_vendidos():
    if 'username' in session:
        produc = []
        cantidad = 5 #elijo aca la cantida de productos que deselo listar
#        registros = class_csv.classificar(nombre_de_archivo)
        produc = func_listar.prod_vendidos(registros = registros, cantidad=cantidad)
        return render_template('prod_vendidos.html', produc = produc)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#--------------------MEJORES CLIENTES----------------

@app.route('/mej_clientes', methods=['GET', 'POST'])
def mej_clientes():
    if 'username' in session:
        produc = []
        cantidad = 5 #elijo aca la cantida de productos que deselo listar
#        registros = class_csv.classificar(nombre_de_archivo)
        produc = func_listar.clientes_gastadores(registros = registros, cantidad=cantidad)
        return render_template('mej_clientes.html', produc = produc)
    else:
        flash('Para Acceder debe Loguearse')
        return redirect(url_for('ingresar'))

#----------------------------------------------------
#clase principal de flask

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug=True)
    manager.run()
