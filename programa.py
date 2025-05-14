import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox

# Configuración de MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_PATH = "C:/xampp/mysql/bin/mysql.exe"  # Cambia si usas otra ruta
NOMBRE_DB = "fichaje_db"
ARCHIVO_SQL = os.path.abspath("fichaje_db.sql")  # Se espera en misma carpeta que este script

# Ruta de origen y destino de carpeta "App-fichaje"
CARPETA_ORIGEN = os.path.abspath("App-fichaje")
DESTINO = r"C:\xampp\htdocs\App-fichaje"

def copiar_carpeta():
    if not os.path.exists(CARPETA_ORIGEN):
        messagebox.showerror("Error", f"La carpeta de origen no existe:\n{CARPETA_ORIGEN}")
        return

    if os.path.exists(DESTINO):
        respuesta = messagebox.askyesno("Carpeta ya existe", "La carpeta ya existe en el destino.\n¿Deseas reemplazarla?")
        if not respuesta:
            messagebox.showinfo("Cancelado", "Operación cancelada por el usuario.")
            return
        try:
            shutil.rmtree(DESTINO)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la carpeta existente:\n{e}")
            return

    try:
        shutil.copytree(CARPETA_ORIGEN, DESTINO)
        messagebox.showinfo("Éxito", "La carpeta fue copiada con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo copiar la carpeta:\n{e}")

def importar_sql():
    if not os.path.exists(ARCHIVO_SQL):
        messagebox.showerror("Error", f"No se encontró el archivo SQL:\n{ARCHIVO_SQL}")
        return

    if not os.path.exists(MYSQL_PATH):
        messagebox.showerror("Error", f"No se encontró mysql.exe en:\n{MYSQL_PATH}")
        return

    # Crear base de datos
    create_db_command = f'"{MYSQL_PATH}" -u{MYSQL_USER} {"-p" + MYSQL_PASSWORD if MYSQL_PASSWORD else ""} -e "CREATE DATABASE IF NOT EXISTS {NOMBRE_DB};"'
    import_command = f'"{MYSQL_PATH}" -u{MYSQL_USER} {"-p" + MYSQL_PASSWORD if MYSQL_PASSWORD else ""} {NOMBRE_DB} < "{ARCHIVO_SQL}"'

    try:
        subprocess.run(create_db_command, shell=True, check=True)
        result = subprocess.run(import_command, shell=True, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            messagebox.showinfo("Éxito", f"La base de datos '{NOMBRE_DB}' fue importada correctamente.")
        else:
            messagebox.showerror("Error al importar", f"Ocurrió un error al importar:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error MySQL", str(e))

# Interfaz gráfica
root = tk.Tk()
root.title("Sistema de Copia e Importación")
root.geometry("400x250")

# Paso 1
label_paso1 = tk.Label(root, text="Paso UNO: Copiar carpeta 'pepe'", font=("Arial", 10, "bold"))
label_paso1.pack(pady=(15, 5))

btn_copiar = tk.Button(root, text="Copiar carpeta 'App-fichaje'", command=copiar_carpeta, width=30, height=2)
btn_copiar.pack()

# Paso 2
label_paso2 = tk.Label(root, text="Paso DOS: Importar a base de datos", font=("Arial", 10, "bold"))
label_paso2.pack(pady=(20, 5))

btn_importar = tk.Button(root, text="Importar archivo SQL a 'fichaje_db'", command=importar_sql, width=30, height=2)
btn_importar.pack()

root.mainloop()
