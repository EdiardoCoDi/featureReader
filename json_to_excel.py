import os
import json
import pandas as pd

def json_to_excel(json_path, excel_path):
    # Leer el archivo JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(data)
    
    # Guardar el DataFrame como un archivo Excel
    df.to_excel(excel_path, index=False)
    print(f"Archivo Excel generado: {excel_path}")

def main():
    directory = input("Introduce la ruta del directorio: ")
    json_path = os.path.join(directory, "feature_report.json")
    excel_path = os.path.join(directory, "feature_report.xlsx")
    
    # Verificar si el archivo JSON existe
    if os.path.exists(json_path):
        json_to_excel(json_path, excel_path)
    else:
        print(f"No se encontró el archivo JSON en la ruta: {json_path}")

if __name__ == "__main__":
    main()
