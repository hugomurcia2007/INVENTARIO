import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os

# Ruta del archivo CSV para guardar el inventario
archivo_inventario = "inventario.csv"

# Variable global para rastrear las ganancias totales
ganancias_totales = 0

# Función para cargar el inventario desde un archivo CSV si existe
def cargar_inventario():
    global inventario
    if os.path.exists(archivo_inventario):
        inventario = pd.read_csv(archivo_inventario)
    else:
        inventario = pd.DataFrame(columns=['Nombre', 'Cantidad', 'Precio', 'Vendidas'])

# Llamar a cargar_inventario al inicio
cargar_inventario()

# Función para guardar el inventario en un archivo CSV
def guardar_inventario():
    inventario.to_csv(archivo_inventario, index=False)

def actualizar_tabla():
    # Limpiar la tabla
    for i in tabla.get_children():
        tabla.delete(i)
    # Insertar los datos del DataFrame en la tabla
    for index, row in inventario.iterrows():
        tabla.insert('', 'end', values=(row['Nombre'], row['Cantidad'], row['Precio'], row['Vendidas'], row['Ganancias']))

def agregar_producto():
    nombre = entry_nombre.get()
    
    # Verificar si los campos de cantidad y precio contienen valores válidos
    try:
        cantidad = int(entry_cantidad.get())
        precio = float(entry_precio.get())
        
        # Verificar que sean valores positivos
        if cantidad <= 0 or precio <= 0:
            messagebox.showerror("Error", "La cantidad y el precio deben ser valores positivos.")
            return
        
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un valor numérico válido en cantidad y precio.")
        return
    
    global inventario
    # Verificar si el producto ya existe en el inventario
    if nombre in inventario['Nombre'].values:
        messagebox.showinfo("Aviso", "El producto ya existe en el inventario. Actualizando cantidad.")
        # Actualizar la cantidad del producto existente
        inventario.loc[inventario['Nombre'] == nombre, 'Cantidad'] += cantidad
    else:
        # Agregar el nuevo producto al inventario
        nuevo_producto = pd.DataFrame({'Nombre': [nombre], 'Cantidad': [cantidad], 'Precio': [precio], 'Vendidas': [0], 'Ganancias': [0]})
        inventario = pd.concat([inventario, nuevo_producto], ignore_index=True)
    messagebox.showinfo("Aviso", "Producto agregado al inventario.")
    actualizar_tabla()
    guardar_inventario()

def quitar_producto():
    nombre = entry_nombre.get()
    
    global inventario
    # Verificar si el producto está en el inventario
    if nombre in inventario['Nombre'].values:
        inventario = inventario[inventario['Nombre'] != nombre]
        messagebox.showinfo("Aviso", "Producto eliminado del inventario.")
    else:
        messagebox.showinfo("Aviso", "El producto no está en el inventario.")
    actualizar_tabla()
    guardar_inventario()

def agregar_venta():
    nombre = entry_nombre.get()
    
    # Verificar si el campo de cantidad contiene un valor válido
    try:
        cantidad = int(entry_cantidad.get())
        
        # Verificar que la cantidad sea positiva
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un valor positivo.")
            return
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un valor numérico válido en cantidad.")
        return
    
    global inventario, ganancias_totales
    # Verificar si el producto está en el inventario
    if nombre in inventario['Nombre'].values:
        # Verificar si la cantidad a vender es menor o igual a la cantidad en el inventario
        if cantidad <= inventario.loc[inventario['Nombre'] == nombre, 'Cantidad'].values[0]:
            # Calcular las ganancias al vender el producto
            precio_producto = inventario.loc[inventario['Nombre'] == nombre, 'Precio'].values[0]
            ganancias = cantidad * precio_producto
            ganancias_totales += ganancias
            messagebox.showinfo("Aviso", f"Ganancias obtenidas por la venta: ${ganancias:.2f}")
            
            # Actualizar la cantidad del producto en el inventario y las unidades vendidas
            inventario.loc[inventario['Nombre'] == nombre, 'Cantidad'] -= cantidad
            inventario.loc[inventario['Nombre'] == nombre, 'Vendidas'] += cantidad
            inventario.loc[inventario['Nombre'] == nombre, 'Ganancias'] += ganancias
            messagebox.showinfo("Aviso", "Cantidad del producto reducida en el inventario.")
        else:
            messagebox.showinfo("Aviso", "No hay suficiente cantidad del producto en el inventario.")
    else:
        messagebox.showinfo("Aviso", "El producto no está en el inventario.")
    actualizar_tabla()
    guardar_inventario()

def mostrar_inventario():
    ventana_inventario = tk.Toplevel(ventana)
    ventana_inventario.title("Inventario Actual")
    
    tabla_inventario = ttk.Treeview(ventana_inventario, columns=('Nombre', 'Cantidad', 'Precio', 'Vendidas', 'Ganancias'))
    tabla_inventario.heading('#0', text='ID')
    tabla_inventario.heading('Nombre', text='Nombre')
    tabla_inventario.heading('Cantidad', text='Cantidad')
    tabla_inventario.heading('Precio', text='Precio')
    tabla_inventario.heading('Vendidas', text='Unidades Vendidas')
    tabla_inventario.heading('Ganancias', text='Ganancias')
    tabla_inventario.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    for index, row in inventario.iterrows():
        tabla_inventario.insert('', 'end', values=(row['Nombre'], row['Cantidad'], row['Precio'], row['Vendidas'], row['Ganancias']))

    # Mostrar las ganancias totales
    label_ganancias = tk.Label(ventana_inventario, text=f"Ganancias Totales: ${ganancias_totales:.2f}")
    label_ganancias.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Inventario al instante")

# Etiquetas y entradas para nombre, cantidad y precio del producto
etiqueta_nombre = tk.Label(ventana, text="Nombre del producto:")
etiqueta_nombre.grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

etiqueta_cantidad = tk.Label(ventana, text="Cantidad:")
etiqueta_cantidad.grid(row=1, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(ventana)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

etiqueta_precio = tk.Label(ventana, text="Precio:")
etiqueta_precio.grid(row=2, column=0, padx=5, pady=5)
entry_precio = tk.Entry(ventana)
entry_precio.grid(row=2, column=1, padx=5, pady=5)

# Botones para agregar, quitar productos y agregar ventas
boton_agregar = tk.Button(ventana, text="Agregar Producto", command=agregar_producto)
boton_agregar.grid(row=3, column=0, padx=5, pady=5, sticky="we")

boton_quitar = tk.Button(ventana, text="Eliminar Producto", command=quitar_producto)
boton_quitar.grid(row=3, column=1, padx=5, pady=5, sticky="we")

boton_agregar_venta = tk.Button(ventana, text="Agregar Venta", command=agregar_venta)
boton_agregar_venta.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Botón para mostrar el inventario
boton_mostrar_inventario = tk.Button(ventana, text="Mostrar Inventario", command=mostrar_inventario)
boton_mostrar_inventario.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Crear y configurar la tabla para mostrar el inventario
tabla = ttk.Treeview(ventana, columns=('Nombre', 'Cantidad', 'Precio', 'Vendidas', 'Ganancias'))
tabla.heading('#0', text='ID')
tabla.heading('Nombre', text='Nombre')
tabla.heading('Cantidad', text='Cantidad')
tabla.heading('Precio', text='Precio')
tabla.heading('Vendidas', text='Unidades Vendidas')
tabla.heading('Ganancias', text='Ganancias')
tabla.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
