import json
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    contra = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegistroForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    contra = PasswordField('Contraseña', validators=[DataRequired()])
    rol = SelectField('Rol', choices=[('admin', 'Administrador'), ('chef', 'Chef')], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class AgregarRecetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    tiempo_preparacion = StringField('Tiempo de Preparación (horas)', validators=[DataRequired()])
    personas = StringField('Número de Personas', validators=[DataRequired()])
    ingredientes = StringField('Ingredientes (nombre1:cantidad1,nombre2:cantidad2,...)', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Agregar Receta')

class EditarRecetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    tiempo_preparacion = StringField('Tiempo de Preparación (horas)', validators=[DataRequired()])
    personas = StringField('Número de Personas', validators=[DataRequired()])
    ingredientes = StringField('Ingredientes (nombre1:cantidad1,nombre2:cantidad2,...)', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')

class MercedarioRecetas:
    def __init__(self):
        self.recetas = {}
        self.usuarios = {}
        self.load_data()
        self.ingredientes = {}  

    def load_data(self):
        try:
            with open("recetas.json", "r") as file:
                data = json.load(file)
                self.recetas = data.get('recetas', {})
                self.usuarios = data.get('usuarios', {})
                self.ingredientes = data.get('ingredientes', {})
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("recetas.json", "w") as file:
            data = {'recetas': self.recetas, 'usuarios': self.usuarios, 'ingredientes': self.ingredientes}
            json.dump(data, file)

    def agregar_receta(self, nombre, tiempo_preparacion, personas, ingredientes, descripcion):
        if nombre not in self.recetas:
            ingredientes_dict = {}
            if ingredientes:
                ingredientes_list = ingredientes.split(',')
                for item in ingredientes_list:
                    parts = item.split(':')
                    if len(parts) == 2:
                        nombre_ingrediente, cantidad = parts
                        ingredientes_dict[nombre_ingrediente.strip()] = cantidad.strip()

            self.recetas[nombre] = {
                'tiempo_preparacion': tiempo_preparacion,
                'personas': personas,
                'ingredientes': ingredientes_dict,
                'descripcion': descripcion
            }
            self.save_data()
            return True
        return False

    def editar_receta(self, nombre, nuevo_nombre, nuevo_tiempo, nuevas_personas, nuevos_ingredientes, nueva_descripcion):
        if nombre in self.recetas:
            receta = self.recetas[nombre]
            del self.recetas[nombre]

            receta['nombre'] = nuevo_nombre
            receta['tiempo_preparacion'] = nuevo_tiempo
            receta['personas'] = nuevas_personas

            if nuevos_ingredientes:
                ingredientes_dict = {}
                ingredientes_list = nuevos_ingredientes.split(',')
                for item in ingredientes_list:
                    parts = item.split(':')
                    if len(parts) == 2:
                        nombre_ingrediente, cantidad = parts
                        ingredientes_dict[nombre_ingrediente.strip()] = cantidad.strip()
                receta['ingredientes'] = ingredientes_dict

            receta['descripcion'] = nueva_descripcion

            self.recetas[nuevo_nombre] = receta
            self.save_data()
            return True

        return False

    def eliminar_receta(self, nombre):
        if nombre in self.recetas:
            del self.recetas[nombre]
            self.save_data()

    def agregar_ingredientes(self, nombre, unidad, valor_unidad, sitio_compra, calorias):
        self.ingredientes[nombre] = {
            'unidad': unidad,
            'valor_unidad': valor_unidad,
            'sitio_compra': sitio_compra,
            'calorias': calorias
        }
        self.save_data()

    def registrar_usuario(self, usuario, contra, rol):
        self.usuarios[usuario] = {
            'contra': generate_password_hash(contra),
            'rol': rol
        }
        self.save_data()

    def iniciar_sesion(self, usuario, contra):
        if usuario in self.usuarios and check_password_hash(self.usuarios[usuario]['contra'], contra):
            return self.usuarios[usuario]['rol']
        return None

    def ver_recetas(self, usuario_actual):
        if not self.recetas:
            return "No hay recetas registradas."

        result = ""
        for nombre, info in self.recetas.items():
            result += f"\n{nombre}:\n"
            result += f"Tiempo de preparación: {info['tiempo_preparacion']} horas\n"
            result += f"Personas: {info['personas']}\n"
            result += "Ingredientes:\n"

            if isinstance(info['ingredientes'], dict):
                for ingrediente, cantidad in info['ingredientes'].items():
                    result += f"- {ingrediente}: {cantidad}\n"
            else:
                result += "- Error en los datos de ingredientes\n"

            result += f"Descripción: {info['descripcion']}\n"

        return result

# Crea una instancia de MercedarioRecetas
mercedario_app = MercedarioRecetas()

# Rutas de Flask

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = form.usuario.data
        contra = form.contra.data

        rol = mercedario_app.iniciar_sesion(usuario, contra)

        if rol:
            session['usuario_actual'] = usuario
            return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    usuario_actual = session.get('usuario_actual')
    if usuario_actual:
        return render_template('dashboard.html', recetas=mercedario_app.recetas, usuario_actual=usuario_actual)
    else:
        return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        usuario = form.usuario.data
        contra = form.contra.data
        rol = form.rol.data

        mercedario_app.registrar_usuario(usuario, contra, rol)
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)

@app.route('/agregar_receta', methods=['GET', 'POST'])
def agregar_receta():
    form = AgregarRecetaForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        tiempo_preparacion = form.tiempo_preparacion.data
        personas = form.personas.data
        ingredientes = form.ingredientes.data
        descripcion = form.descripcion.data

        mercedario_app.agregar_receta(nombre, tiempo_preparacion, personas, ingredientes, descripcion)
        return redirect(url_for('dashboard'))

    return render_template('agregar_receta.html', form=form)

@app.route('/editar_receta/<nombre>', methods=['GET', 'POST'])
def editar_receta(nombre):
    receta_existente = mercedario_app.recetas.get(nombre)

    if receta_existente:
        form = EditarRecetaForm(obj=receta_existente)

        if form.validate_on_submit():
            nuevo_nombre = form.nombre.data
            nuevo_tiempo = form.tiempo_preparacion.data
            nuevas_personas = form.personas.data
            nuevos_ingredientes = form.ingredientes.data
            nueva_descripcion = form.descripcion.data

            if mercedario_app.editar_receta(nombre, nuevo_nombre, nuevo_tiempo, nuevas_personas, nuevos_ingredientes, nueva_descripcion):
                return redirect(url_for('dashboard'))
            else:
                flash("Error al editar la receta. La receta no existe.", 'error')

        return render_template('editar_receta.html', form=form, nombre_receta=nombre)

    else:
        flash("Error al cargar la receta. La receta no existe.", 'error')
        return redirect(url_for('dashboard'))

@app.route('/eliminar_receta/<nombre>', methods=['POST'])
def eliminar_receta(nombre):
    if request.method == 'POST':
        if mercedario_app.eliminar_receta(nombre):
            flash(f"Receta {nombre} eliminada exitosamente", 'success')
        else:
            flash(f"No se pudo encontrar la receta {nombre}", 'error')

    return redirect(url_for('dashboard'))

@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    if 'usuario_actual' in session:
        session.pop('usuario_actual')
    return redirect(url_for('index'))

@app.route('/ingredientes', methods=['GET'])
def ingredientes():
    return render_template('ingredientes.html', ingredientes=mercedario_app.ingredientes)

@app.route('/ver_ingredientes')
def ver_ingredientes():
    return render_template('ver_ingredientes.html', ingredientes=mercedario_app.ingredientes)


@app.route('/agregar_ingredientes', methods=['GET', 'POST'])
def agregar_ingredientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        unidad = request.form['unidad']
        valor_unidad = request.form['valor_unidad']
        sitio_compra = request.form['sitio_compra']
        calorias = request.form['calorias']

        if mercedario_app.agregar_ingredientes(nombre, unidad, valor_unidad, sitio_compra, calorias):
            flash(f"Ingrediente {nombre} agregado exitosamente", 'success')
        else:
            flash(f"El ingrediente {nombre} ya existe", 'error')

        return redirect(url_for('agregar_ingredientes'))

    return render_template('agregar_ingredientes.html')

@app.route('/editar_ingrediente/<nombre>', methods=['GET', 'POST'])
def editar_ingrediente(nombre):
    if request.method == 'POST':
        unidad = request.form['unidad']
        valor_unidad = request.form['valor_unidad']
        sitio_compra = request.form['sitio_compra']
        calorias = request.form['calorias']

        if mercedario_app.editar_ingrediente(nombre, unidad, valor_unidad, sitio_compra, calorias):
            flash(f"Ingrediente {nombre} editado exitosamente", 'success')
        else:
            flash(f"No se pudo editar el ingrediente {nombre}", 'error')

        return redirect(url_for('ingredientes'))

    ingrediente_info = mercedario_app.ingredientes.get(nombre, {})
    return render_template('editar_ingrediente.html', nombre=nombre, ingrediente_info=ingrediente_info)

@app.route('/borrar_ingrediente/<nombre>', methods=['POST'])
def borrar_ingrediente(nombre):
    if request.method == 'POST':
        if mercedario_app.borrar_ingrediente(nombre):
            flash(f"Ingrediente {nombre} eliminado exitosamente", 'success')
        else:
            flash(f"No se pudo borrar el ingrediente {nombre}", 'error')

    return redirect(url_for('ingredientes'))

if __name__ == '__main__':
    app.run(debug=True)
