import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient
from bson import ObjectId

# ===== CONEXION A MONGODB ATLAS =====
Mongo_User = "hector1985"
Mongo_Password = "Aime131985"
Mongo_Cluster = "utvt.qqqotrr.mongodb.net"
Mongo_db = "juan_d73"
Mongo_Colleccion = "diagnostico"

uri = "mongodb+srv://" + Mongo_User + ":" + Mongo_Password + "@" + Mongo_Cluster + "/?retryWrites=true&w=majority"
cliente = MongoClient(uri)
base = cliente[Mongo_db]
coleccion = base[Mongo_Colleccion]

documentos = {}
seleccionado = None

ventana = tk.Tk()
ventana.title("SISTEMA DE DIAGNOSTICO HOSPITALARIO")
ventana.geometry("720x880")
ventana.config(bg="white")
ventana.iconphoto(False, tk.PhotoImage(width=1, height=1))

tk.Label(ventana, text="+ SISTEMA DE DIAGNOSTICO HOSPITALARIO", font=("Arial", 16, "bold"), bg="#8b1e2d", fg="white", pady=12).pack(fill="x")
tk.Label(ventana, text="Registro de paciente y signos vitales", font=("Arial", 10), bg="#f2f2f2", fg="#555555", pady=5).pack(fill="x")

datos = tk.Frame(ventana, bg="white", relief="solid", bd=1)
datos.pack(padx=20, pady=15)

tk.Label(datos, text="Nombre:", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=0, column=0, padx=8, pady=6)
nombre = tk.Entry(datos, font=("Arial", 10), width=18)
nombre.grid(row=0, column=1, padx=8, pady=6)

tk.Label(datos, text="Edad:", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=0, column=2, padx=8, pady=6)
edad = tk.Entry(datos, font=("Arial", 10), width=18)
edad.grid(row=0, column=3, padx=8, pady=6)

tk.Label(datos, text="Oxigenacion (%):", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=1, column=0, padx=8, pady=6)
oxigenacion = tk.Entry(datos, font=("Arial", 10), width=18)
oxigenacion.grid(row=1, column=1, padx=8, pady=6)

tk.Label(datos, text="Frecuencia cardiaca (lpm):", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=1, column=2, padx=8, pady=6)
frecuencia = tk.Entry(datos, font=("Arial", 10), width=18)
frecuencia.grid(row=1, column=3, padx=8, pady=6)

tk.Label(datos, text="Presion arterial (mmHg):", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=2, column=0, padx=8, pady=6)
presion = tk.Entry(datos, font=("Arial", 10), width=18)
presion.grid(row=2, column=1, padx=8, pady=6)

tk.Label(datos, text="Peso (kg):", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=2, column=2, padx=8, pady=6)
peso = tk.Entry(datos, font=("Arial", 10), width=18)
peso.grid(row=2, column=3, padx=8, pady=6)

tk.Label(datos, text="Talla (cm):", bg="white", font=("Arial", 10), anchor="e", width=22).grid(row=3, column=0, padx=8, pady=6)
talla = tk.Entry(datos, font=("Arial", 10), width=18)
talla.grid(row=3, column=1, padx=8, pady=6)

def num(texto):
    try:
        return int(texto)
    except ValueError:
        try:
            return float(texto)
        except ValueError:
            return texto

def leer_paciente():
    return {
        "nombre": nombre.get(),
        "edad": num(edad.get()),
        "oxigenacion": num(oxigenacion.get()),
        "frecuencia": num(frecuencia.get()),
        "presion": num(presion.get()),
        "peso": num(peso.get()),
        "talla": num(talla.get())
    }

def insertar():
    doc = leer_paciente()
    doc["diagnostico"] = resultado.get("1.0", "end").strip()
    try:
        coleccion.insert_one(doc)
        mostrar()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo guardar: " + str(e))

def mostrar():
    for fila in tabla.get_children():
        tabla.delete(fila)
    documentos.clear()
    try:
        par = True
        for doc in coleccion.find().sort("_id", -1):
            iid = str(doc["_id"])
            documentos[iid] = doc
            tabla.insert("", "end", iid=iid, values=(
                doc.get("nombre", ""),
                doc.get("edad", ""),
                doc.get("oxigenacion", ""),
                doc.get("frecuencia", ""),
                doc.get("presion", ""),
                doc.get("peso", ""),
                doc.get("talla", "")
            ), tags=("par" if par else "impar",))
            par = not par
    except Exception as e:
        messagebox.showerror("Error", "No se pudo leer la base: " + str(e))

def seleccionar(event):
    global seleccionado
    sel = tabla.selection()
    if not sel:
        return
    seleccionado = sel[0]
    doc = documentos.get(seleccionado, {})
    for entrada, campo in [(nombre, "nombre"), (edad, "edad"), (oxigenacion, "oxigenacion"),
                           (frecuencia, "frecuencia"), (presion, "presion"),
                           (peso, "peso"), (talla, "talla")]:
        entrada.delete(0, "end")
        entrada.insert(0, str(doc.get(campo, "")))

def actualizar():
    if not seleccionado:
        messagebox.showwarning("Atencion", "Selecciona un registro de la tabla")
        return
    try:
        coleccion.update_one({"_id": ObjectId(seleccionado)}, {"$set": leer_paciente()})
        mostrar()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo actualizar: " + str(e))

def eliminar():
    global seleccionado
    if not seleccionado:
        messagebox.showwarning("Atencion", "Selecciona un registro de la tabla")
        return
    if not messagebox.askyesno("Eliminar", "Eliminar el registro seleccionado del Atlas?"):
        return
    try:
        coleccion.delete_one({"_id": ObjectId(seleccionado)})
        seleccionado = None
        mostrar()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo eliminar: " + str(e))

def diagnosticar():
    P = int(oxigenacion.get()) < 90
    Q = int(frecuencia.get()) < 60 or int(frecuencia.get()) > 100
    R = int(presion.get()) > 140

    imc = float(peso.get()) / (float(talla.get()) / 100) ** 2
    S = imc >= 25

    texto = "Diagnostico:\n"

    if P:
        texto += "Sintoma: oxigenacion baja\nRecomendacion: administrar oxigeno y mantener al paciente en reposo\n"
    if Q:
        texto += "Sintoma: frecuencia cardiaca fuera de rango\nRecomendacion: descansar\n"
    if R:
        texto += "Sintoma: presion arterial alta\nRecomendacion: reducir sal\n"
    if S:
        texto += "Sintoma: sobrepeso (IMC alto)\nRecomendacion: mejorar la dieta y hacer ejercicio\n"

    cantidad = P + Q + R + S

    if cantidad == 0:
        texto += "\nNivel de riesgo: bajo\n"
        texto += "Estado: paciente estable, continuar con revisiones de rutina\n"
    elif cantidad <= 2:
        texto += "\nNivel de riesgo: medio\n"
        texto += "ADVERTENCIA: el paciente debe acudir a consulta medica\n"
    else:
        texto += "\nNivel de riesgo: alto\n"
        texto += "PELIGRO: el paciente debe ser atendido en urgencias\n"

    numero_cita = random.randint(1, 20)

    texto += "\nCita generada:\n"
    texto += "Numero de cita: " + str(numero_cita) + "\n"
    texto += "Fecha: " + str(numero_cita) + "/10/2026\n"
    texto += "Hora: 10:00\n"
    texto += "\nResumen del paciente:\n"
    texto += "Nombre: " + nombre.get() + "\n"
    texto += "Edad: " + edad.get() + "\n"
    texto += "Sintomas detectados: " + str(cantidad)

    resultado.delete("1.0", "end")
    resultado.insert("end", texto)

    insertar()

botones = tk.Frame(ventana, bg="white")
botones.pack(pady=(0, 10))

tk.Button(botones, text="Diagnosticar y guardar", command=diagnosticar, bg="#8b1e2d", fg="white", font=("Arial", 10, "bold"), padx=12, pady=6).grid(row=0, column=0, padx=5)
tk.Button(botones, text="Actualizar", command=actualizar, bg="#1e5a8b", fg="white", font=("Arial", 10, "bold"), padx=12, pady=6).grid(row=0, column=1, padx=5)
tk.Button(botones, text="Eliminar", command=eliminar, bg="#555555", fg="white", font=("Arial", 10, "bold"), padx=12, pady=6).grid(row=0, column=2, padx=5)
tk.Button(botones, text="Mostrar registros", command=mostrar, bg="#2d7a4f", fg="white", font=("Arial", 10, "bold"), padx=12, pady=6).grid(row=0, column=3, padx=5)

tk.Label(ventana, text="Tabla de registros", font=("Arial", 12, "bold"), bg="white", fg="#8b1e2d", anchor="w").pack(fill="x", padx=20)

estilo = ttk.Style(ventana)
estilo.theme_use("clam")
estilo.configure("Treeview",
                 background="white",
                 foreground="#333333",
                 fieldbackground="white",
                 rowheight=26,
                 font=("Arial", 10))
estilo.configure("Treeview.Heading",
                 background="#8b1e2d",
                 foreground="white",
                 font=("Arial", 10, "bold"),
                 padding=6,
                 relief="flat")
estilo.map("Treeview",
           background=[("selected", "#c94f60")],
           foreground=[("selected", "white")])
estilo.map("Treeview.Heading",
           background=[("active", "#6d1623")])

tabla_frame = tk.Frame(ventana, bg="white", relief="solid", bd=1)
tabla_frame.pack(fill="x", padx=20, pady=(5, 10))

barra_tabla = ttk.Scrollbar(tabla_frame, orient="vertical")
barra_tabla.pack(side="right", fill="y")

tabla = ttk.Treeview(tabla_frame, columns=("nombre", "edad", "oxigenacion", "frecuencia", "presion", "peso", "talla"), show="headings", height=6, yscrollcommand=barra_tabla.set)
tabla.heading("nombre", text="Nombre")
tabla.heading("edad", text="Edad")
tabla.heading("oxigenacion", text="Oxigenacion")
tabla.heading("frecuencia", text="Frecuencia")
tabla.heading("presion", text="Presion")
tabla.heading("peso", text="Peso")
tabla.heading("talla", text="Talla")
tabla.column("nombre", width=160)
tabla.column("edad", width=60, anchor="center")
tabla.column("oxigenacion", width=100, anchor="center")
tabla.column("frecuencia", width=100, anchor="center")
tabla.column("presion", width=90, anchor="center")
tabla.column("peso", width=75, anchor="center")
tabla.column("talla", width=75, anchor="center")
tabla.tag_configure("par", background="#ffffff")
tabla.tag_configure("impar", background="#f5e6e8")
tabla.pack(fill="x")
tabla.bind("<<TreeviewSelect>>", seleccionar)

barra_tabla.config(command=tabla.yview)

tk.Label(ventana, text="Hoja de diagnostico", font=("Arial", 12, "bold"), bg="white", fg="#8b1e2d", anchor="w").pack(fill="x", padx=20)

hoja = tk.Frame(ventana, bg="white")
hoja.pack(fill="both", expand=True, padx=20, pady=(5, 20))

barra = tk.Scrollbar(hoja)
barra.pack(side="right", fill="y")

resultado = tk.Text(hoja, font=("Arial", 10), relief="solid", bd=1, padx=10, pady=10, yscrollcommand=barra.set)
resultado.pack(fill="both", expand=True)

barra.config(command=resultado.yview)

ventana.mainloop()
