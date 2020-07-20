from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'sancho'

mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', clientes=data)

# Clientes --------------------------
@app.route('/clientes')
def Clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('clientes.html', clientes=data)


@app.route('/addUser', methods=["POST"])
def addUser():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes')
        data = cur.fetchall()
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        file = request.files['inputfile']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes(nombre, cedula, telefono, direccion) VALUES(%s, %s, %s, %s)',
                    (nombre, cedula, telefono, direccion))
        mysql.connection.commit()

        print(nombre)
        print(cedula)
        print(telefono)
        print(direccion)
        print(file.filename)

        return redirect(url_for('Clientes'))

@app.route('/editcliente/<cedula>')
def get_user(cedula):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE cedula = {0}".format(cedula))
    data = cur.fetchall()
    print(data[0])
    return render_template('editarcliente.html', clientedata=data[0])


@app.route('/deletecliente/<string:cedula>')
def deleteUSer(cedula):
    cur = mysql.connection.cursor()
    cur.execute("DELETE  FROM clientes WHERE cedula = {0}".format(cedula))
    mysql.connection.commit()
    return redirect(url_for("Clientes"))


@app.route('/updatecliente/<cedula>', methods=['POST'])
def updatecliente(cedula):
    if request.method == 'POST':
        #cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
     UPDATE clientes 
     SET          
        nombre = %s, 
        direccion = %s,
        telefono = %s
     WHERE cedula = %s
     """   , (nombre, direccion, telefono, cedula))
        mysql.connection.commit()
        print(cedula)
        return redirect(url_for("Clientes"))

# Productos --------------------------
@app.route('/productos')
def Productos():
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos ')
    cur1.execute('SELECT * FROM productos WHERE estado = "Disponible" ')
    data = cur.fetchall()
    data1 = cur1.fetchall()
    return render_template('productos.html', productos=data, productosD=data1)


@app.route('/addProduct', methods=["POST"])
def addProduct():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM clientes')
        data = cur.fetchall()
        codigo = request.form['codigo']
        categoria = request.form['categoria']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        estado = request.form['estado']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos(codigo, categoria, nombre, precio, cantidad,estado) VALUES(%s, %s, %s, %s, %s, %s)',
                    (codigo, categoria, nombre, precio, cantidad, estado))
        mysql.connection.commit()

        print(codigo)
        print(categoria)
        print(nombre)
        print(precio)
        print(cantidad)
        print(estado)

        return redirect(url_for('Productos'))

@app.route('/editproducto/<codigo>')
def get_codigo(codigo):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE codigo = {0}".format(codigo))
    data = cur.fetchall()
    print(data[0])
    return render_template('editarproducto.html', producto=data[0])        

@app.route('/deleteproducto/<string:codigo>')
def deleteProducto(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE  FROM productos WHERE codigo = {0}".format(codigo))
    mysql.connection.commit()
    return redirect(url_for("Productos"))


@app.route('/updateproducto/<codigo>', methods=['POST'])
def updateproducto(codigo):
    if request.method == 'POST':
        
        categoria = request.form['categoria']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
     UPDATE productos 
     SET          
        categoria = %s, 
        nombre = %s,
        precio = %s,
        cantidad = %s,
        estado = %s
     WHERE codigo = %s
     """   , (categoria, nombre, precio, cantidad,estado,codigo ))
        mysql.connection.commit()
        print(codigo)
        return redirect(url_for("Productos"))    


# Facturas --------------------------
@app.route('/facturas')
def Facturas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM facturas')
    data = cur.fetchall()
    return render_template('facturas.html', facturas=data)


@app.route('/addFactura', methods=["POST"])
def addFactura():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM facturas')
        data = cur.fetchall()
        #codigo = request.form['codigo']
        cliente = request.form['cliente']
        productos = request.form['productos']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        valor = request.form['valor']
        metodo = request.form['metodo']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO facturas( cliente, productos, cantidad, fecha,valor,metodo) VALUES( %s, %s, %s, %s, %s,%s)',
                    (cliente, productos, cantidad, fecha, valor, metodo))
        mysql.connection.commit()

        # print(codigo)
        print(cliente)
        print(productos)
        print(cantidad)
        print(fecha)
        print(valor)
        print(metodo)

        return redirect(url_for('Facturas'))


@app.route('/editfactura/<codigo>')
def get_factura(codigo):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM facturas WHERE codigo = {0}".format(codigo))
    data = cur.fetchall()
    print(data[0])
    return render_template('editarfactura.html', factura=data[0]) 

@app.route('/deletefactura/<string:codigo>')
def deleteFactura(codigo):
    cur = mysql.connection.cursor()
    cur.execute("DELETE  FROM facturas WHERE codigo = {0}".format(codigo))
    mysql.connection.commit()
    return redirect(url_for("Facturas"))

@app.route('/updatefactura/<codigo>', methods=['POST'])
def updatefactura(codigo):
    if request.method == 'POST':
        
        cliente = request.form['cliente']
        productos = request.form['productos']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        valor = request.form['valor']
        metodo = request.form['metodo']
        cur = mysql.connection.cursor()
        cur.execute("""
     UPDATE facturas 
     SET          
        cliente = %s, 
        productos = %s,
        cantidad = %s,
        fecha = %s,
        valor = %s,
        metodo = %s
        
     WHERE codigo = %s
     """   , (cliente, productos, cantidad, fecha,valor,metodo, codigo ))
        mysql.connection.commit()
        print(codigo)
        return redirect(url_for("Facturas"))    


@app.route('/upload')
def upload():
    file = request.files['inputfile']
    return file.filename


if __name__ == "__main__":
    app.run(port=3000, debug=True)
