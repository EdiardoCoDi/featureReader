import os
import json
import pandas as pd
from gherkin.parser import Parser

def find_feature_files(directory):
    feature_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".feature"):
                feature_files.append(os.path.join(root, file))
    print(f"Archivos .feature encontrados: {feature_files}")
    return feature_files

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    print(f"Contenido leído del archivo {file_path}: {content[:500]}")  # Mostrar los primeros 500 caracteres para depurar
    return content

def parse_feature_file(content):
    parser = Parser()
    feature = parser.parse(content)
    print(f"Estructura parseada: {json.dumps(feature, indent=2)}")
    return feature

def extract_scenarios(feature, feature_file):
    report = []
    feature_content = feature.get('feature', {})
    for child in feature_content.get('children', []):
        rule = child.get('rule')
        if rule:
            for element in rule.get('children', []):
                if 'scenario' in element:
                    scenario = element['scenario']
                    element_type = scenario.get('keyword')
                    if element_type in ['Scenario', 'Scenario Outline']:
                        scenario_info = {
                            "ruta del archivo": feature_file,
                            "tags": [tag['name'] for tag in scenario.get('tags', [])],
                            "scenario": scenario['name']
                        }
                        report.append(scenario_info)
                        print(f"Añadiendo escenario: {json.dumps(scenario_info, indent=2)}")
    return report

def generate_report(directory):
    report = []
    feature_files = find_feature_files(directory)
    if not feature_files:
        print("No se encontraron archivos .feature")
        return report  # Retornar un reporte vacío si no se encontraron archivos

    for feature_file in feature_files:
        print(f"Procesando archivo: {feature_file}")
        try:
            content = read_file(feature_file)
            feature = parse_feature_file(content)
            report.extend(extract_scenarios(feature, feature_file))
        except Exception as e:
            print(f"Error procesando el archivo {feature_file}: {e}")
    return report

def json_to_excel(json_path, excel_path):
    try:
        # Leer el archivo JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data)
        
        # Guardar el DataFrame como un archivo Excel
        df.to_excel(excel_path, index=False)
        print(f"Archivo Excel generado: {excel_path}")
    except Exception as e:
        print(f"Error al convertir JSON a Excel: {e}")

def main():
    directory = input("Introduce la ruta del directorio: ")
    report = generate_report(directory)
    print(f"Reporte generado: {json.dumps(report, indent=2)}")  # Depuración: Ver el contenido de report
    
    if report:  # Asegurarse de que el reporte no esté vacío
        report_path = os.path.join(directory, "feature_report.json")
        try:
            with open(report_path, 'w', encoding='utf-8') as report_file:
                json.dump(report, report_file, ensure_ascii=False, indent=4)
            print(f"Reporte generado y guardado en: {report_path}")
            
            # Convertir el JSON a Excel
            excel_path = os.path.join(directory, "feature_report.xlsx")
            json_to_excel(report_path, excel_path)
        except Exception as e:
            print(f"Error al generar el reporte: {e}")
    else:
        print("No se generó ningún reporte porque no se encontraron escenarios.")

if __name__ == "__main__":
    main()
