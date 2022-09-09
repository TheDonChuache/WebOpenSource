'''
Tema: Aplicación de estructuras de Python: archivos, JSON, cifrado de contraseñas
Fecha: 06 de septiembre del 2022
Autor: Carlos Israel Bautista Mejía
Continuación de la práctica 6
'''
import json
import random
import bcrypt

'''
Crear un programa que utilice los archivos Estudiantes.prn y kardex.txt:

1. Crear un método que regrese un conjunto de tuplas de estudiantes. (5) 10 min.
2. Crear un método que regrese un conjunto de tuplas de materias.
3. Crear un método que dado un número de control regrese el siguiente formato JSON:
   {
        "Nombre": "Manzo Avalos Diego",
        "Materias":[
            {
                "Nombre":"Base de Datos",
                "Promedio":85
            },
            {
                "Nombre":"Inteligencia Artificial",
                "Promedio":100
            },
            . . . 
        ],
        "Promedio general": 98.4
   }

4. Regresar una lista de JSON con las materias de un estudiante, el formato es el siguiente:
[
    {"Nombre": "Contabilidad Financiera"},
    {"Nombre": "Dise\u00f1o UX y UI"}, 
    {"Nombre": "Base de datos distribuidas"}, 
    {"Nombre": "Finanzas internacionales IV"}, 
    {"Nombre": "Analisis y dise\u00f1o de sistemas de informacion"}, 
    {"Nombre": "Microservicios"},
    {"Nombre": "Algoritmos inteligentes"}
]
'''
def Estudiantes():          #Ejercicio 1
    archivo = open("Estudiantes.prn", "r")
    conjunto = set()
    for linea in archivo:
        conjunto.add((linea[0:8], linea[8:-1]))

    return conjunto


def Materias():             #Ejercicio 2
    archivo = open("Kardex.txt", "r")
    materias = set()
    for linea in archivo:
        d2 = linea.split("|")
        dato = int(str(d2[2]))
        materias.add((linea[0:8], d2[1], dato))
    archivo.close()
    return materias

def regresa_materias_por_estudiante(ctrl):
    promedios = Materias()
    lista_materias = []
    for mat in promedios:
        c, m, p = mat
        if ctrl == c:
            lista_materias.append({"Nombre:":m})
    return json.dumps(lista_materias)

print(regresa_materias_por_estudiante("18420430"))
'''
5. Generar un archivo de usuarios que contenga el numero de control, éste será el usuario
   y se generará una contraseña de tamaño 10 la cual debe tener:
   A. Al menos una letra mayúscula 
   B. Al menos una letra minúscula
   C. Numeros
   D. Al menos UN carácter especial, considere ( @, #, $,%,&,_,?,! )

   Considere:
    - Crear un método para generar cada caracter
    - El codigo ascii: https://elcodigoascii.com.ar/
    - Cifrar la contraseña con bcrypt, se utiliza con node.js, react, etc. Para ello:
        * Descargue la libreria bcrypt con el comando: "pip install bcrypt" desde la terminal o desde PyCharm
        * Página: https://pypi.org/project/bcrypt/
        * Video:Como Cifrar Contraseñas en Python     https://www.youtube.com/watch?v=9tEovDYSPK4

   El formato del archivo usuarios.txt será:
   control contrasena contraseña_cifrada
   
'''

def Generar_mayúscula():            # Regresa letra aleatoria mayúscula
    return chr(random.randint(65, 90))

def Generar_minuscula():            # Regresa letra aleatoria minúscula
    return chr(random.randint(97,122))

def Generar_numeros():              # Regresa número aleatorio
    return chr(random.randint(48, 57))

def Generar_c_esp():                # Regresa caracter especial aleatorio
    lista_caracteres = ["@", "#", "$", "%", "&", "_", "?", "!"]
    return lista_caracteres[random.randint(0, 7)]

def Generar_pass():
    numero = random.randint(1, 5)
    clave = ""

    if numero == 1:
        clave = Generar_mayúscula()
    if numero == 2:
        clave = Generar_minuscula()
    if numero == 3:
        clave = Generar_c_esp()
    if numero >= 4 and numero <= 5:
        clave = Generar_numeros()

    return clave

clave = ""
for i in range(0, 10):
    clave += Generar_pass()

def Cifrar_password(password):
    sal = bcrypt.gensalt() # Default tiene de 12
    password_encrypted = bcrypt.hashpw(password.encode(), sal)
    return password_encrypted

print(Cifrar_password(clave),"\n",clave)

def Generar_archivo_usuarios():
    # Obtener lista de estudiantes.
    l_estudiantes = list(Estudiantes())
    archivo = open("usuarios.txt", "w")
    cont = 1

    for est in l_estudiantes:
        c, n = est
        clave = ""

        for i in range(0, 10):
            clave += Generar_pass()
        encrypted_password = Cifrar_password(clave)

        registro = c + " " + clave + " "+ str(encrypted_password, "utf-8")+ "\n"

        archivo.write(registro)
        cont += 1
        print(cont)
    print("Archivo generado")

# Generar_archivo_usuarios()

def Authentication():
    archivo = open("usuarios.txt", "r")
    l_estudiantes = list(Estudiantes())
    l_auth = []

    usuario = input("Ingresa el usuario")
    password = input("Ingresa la contraseña")

    ban = False
    nombre = ""
    mensaje = ""

    for est in l_estudiantes:
        if usuario == est[0]:
            nombre = est[1]
            break
        else:
            nombre=""
            mensaje = "No existe el usuario"

    for linea in archivo:
        l_auth = linea.split(" ")
        l_auth[2] = l_auth[2][:-1]
        if usuario == l_auth[0]:
            if bcrypt.checkpw(password.encode("utf-8"), l_auth[2].encode("utf-8")):
                mensaje = "Bienvenido al Sistema de Autenticación de usuarios"
                ban = True
            else:
                ban = False
                mensaje = "Contraseña incorrecta"

    # print()
    # print("Bandera: ",ban)
    # print("Usuario: ", nombre)
    # print("Mensaje: ", mensaje)
    dicc = {"Bandera":ban, "Nombre":nombre, "Mensaje":mensaje}
    return json.dumps(dicc, indent=3)

print(Authentication())

'''
6. Crear un método "autenticar_usuario(usuario,contrasena)" que regrese una bandera que 
   indica si se pudo AUTENTICAR, el nombre del estudiante y un mensaje, regresar el JSON:
   {
        "Bandera": True,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Bienvenido al Sistema de Autenticación de usuarios"
   }

   ó

   {
        "Bandera": False,
        "Usuario": "",
        "Mensaje": "No existe el Usuario"
   }

   ó

    {
        "Bandera": False,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Contraseña incorrecta"
   }


'''
