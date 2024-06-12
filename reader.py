import os
import json
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
            feature_content = feature.get('feature', {})
            for element in feature_content.get('children', []):
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
        except Exception as e:
            print(f"Error procesando el archivo {feature_file}: {e}")
    return report

def main():
    directory = input("Introduce la ruta del directorio: ")
    report = generate_report(directory)
    print(f"Reporte generado: {json.dumps(report, indent=2)}")  # Depuración: Ver el contenido de report
    if report:  # Asegurarse de que el reporte no esté vacío
        report_path = os.path.join(directory, "feature_report.json")
        with open(report_path, 'w', encoding='utf-8') as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=4)
        print(f"Reporte generado: {report_path}")
    else:
        print("No se generó ningún reporte porque no se encontraron escenarios.")

if __name__ == "__main__":
    main()
