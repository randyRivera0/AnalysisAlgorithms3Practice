# Stoogesort implementation with timing and data loading
# Referencia: https://en.wikipedia.org/wiki/Stooge_sort
# Nombre completo: Randy Adley Rivera Bermudez
# Paralelo: 1/101
# Fecha de realización: 12/11/2024


import time
import random
import numpy as np
import pandas as pd
import sys
import itertools
import os


def stoogesort(arr, l, h, spinner, depth=0):
    if l >= h:
        return
    
    if arr[l] > arr[h]:
        arr[l], arr[h] = arr[h], arr[l]
    
    if h - l + 1 > 2:
        t = (h - l + 1) // 3
        
        # Print the next spinner character for progress
        sys.stdout.write(f"\r{next(spinner)}")
        sys.stdout.flush()
        
        stoogesort(arr, l, h - t, spinner, depth + 1)
        stoogesort(arr, l + t, h, spinner, depth + 1)
        stoogesort(arr, l, h - t, spinner, depth + 1)


# Load data from file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = list(map(int, file.read().split()))
    return np.array(data)


# Check if the array is sorted
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


# Main function to run the sorting and measure time
def measure_execution_time(file_path):
    data = load_data(file_path)
    n = len(data)
    print(f"Sorting {n} elements:")   
    spinner = itertools.cycle(['|', '/', '-', '\\'])  # Creates a cycle of characters
    start_time = time.time()
    stoogesort(data, 0, n - 1, spinner)
    end_time = time.time()
    execution_time = end_time - start_time
     # Verify if the array is sorted and print the result
    if is_sorted(data):
        print("\nArray is sorted correctly.")
    else:
        print("\nArray is NOT sorted correctly.")
    
    # Print the sorted array
    print("Sorted array:", data)
    print(f"Execution time for {n} elements: {execution_time:.4f} seconds")
    return n, execution_time


def generar_datos(nombre_archivo, cantidad, rango=(1, 1000)):
    """
    Genera un archivo con números aleatorios para usar en Stoogesort, solo si el archivo no existe.

    Parámetros:
        nombre_archivo (str): Nombre del archivo donde se guardarán los datos, por ejemplo, 'data1.dat'.
        cantidad (int): Número de elementos que se generarán.
        rango (tuple): Rango de los números aleatorios (valor mínimo, valor máximo).

    Ejemplo de uso:
        generar_datos("data1.dat", 100)  # Crea un archivo con 100 números aleatorios entre 1 y 1000.
    """
    # Verifica si el archivo ya existe
    if not os.path.exists(nombre_archivo):
        print(f"Generando el archivo: {nombre_archivo} con {cantidad} números aleatorios.")
        with open(nombre_archivo, 'w') as f:
            # Genera 'cantidad' de números aleatorios dentro del rango dado y escribe en el archivo
            numeros = [str(random.randint(rango[0], rango[1])) for _ in range(cantidad)]
            f.write(" ".join(numeros))
        print(f"Archivo {nombre_archivo} generado exitosamente.")
    else:
        print(f"El archivo {nombre_archivo} ya existe. No se generarán nuevos datos.")


# Ejemplos de uso para generar archivos de diferentes tamaños
generar_datos("data1.dat", 500)     # Genera un archivo con 100 números
generar_datos("data2.dat", 1000)    # Genera un archivo con 1000 números
generar_datos("data3.dat", 2000)   # Genera un archivo con 10,000 números

# Example usage
file_paths = ["data1.dat", "data2.dat", "data3.dat"]
results = [measure_execution_time(file_path) for file_path in file_paths]

# Save results to a table for your PDF
results_df = pd.DataFrame(results, columns=["Data Size", "Execution Time (s)"])
results_df.to_csv("execution_times.csv", index=False)
