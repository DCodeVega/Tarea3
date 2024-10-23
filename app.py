from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_seminarios'  

@app.before_request
def inicializar_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        turno = request.form.get('turno')
        seminarios = request.form.getlist('seminarios')  

        nuevo_inscrito = {
            'id': len(session['inscritos']) + 1,
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': ', '.join(seminarios)  
        }

        inscritos = session['inscritos']
        inscritos.append(nuevo_inscrito)
        session['inscritos'] = inscritos

        return redirect(url_for('ver_inscritos'))
    
    return redirect(url_for('index'))

@app.route('/inscritos')
def ver_inscritos():
    return render_template('listado.html', inscritos=session['inscritos'])

@app.route('/eliminar/<int:id>')
def eliminar(id):
    inscritos = session['inscritos']
    inscritos = [i for i in inscritos if i['id'] != id]
    session['inscritos'] = inscritos
    return redirect(url_for('ver_inscritos'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    inscritos = session['inscritos']
    
    if request.method == 'POST':
        for i in range(len(inscritos)):
            if inscritos[i]['id'] == id:
                inscritos[i]['fecha'] = request.form.get('fecha')
                inscritos[i]['nombre'] = request.form.get('nombre')
                inscritos[i]['apellidos'] = request.form.get('apellidos')
                inscritos[i]['turno'] = request.form.get('turno')
                inscritos[i]['seminarios'] = ', '.join(request.form.getlist('seminarios'))
                break
        
        session['inscritos'] = inscritos
        return redirect(url_for('ver_inscritos'))
    
    inscrito = next((i for i in inscritos if i['id'] == id), None)
    if inscrito:
        return render_template('editar.html', inscrito=inscrito)
    
    return redirect(url_for('ver_inscritos'))

if __name__ == '__main__':
    app.run(debug=True)