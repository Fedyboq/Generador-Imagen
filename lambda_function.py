import json
import tempfile
import os
import base64
import traceback
from eralchemy2 import render_er

def handler(event, context):
    try:
        # Parsear el input
        raw_body = event.get("body", "")
        parsed = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        er_data = parsed.get("body", {})
        
        if not isinstance(er_data, dict) or not er_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El campo 'body' debe contener un objeto JSON con la definición ER"})
            }
        
        # Validar estructura básica
        if "entities" not in er_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El JSON debe contener una lista 'entities'"})
            }
        
        # Generar archivo temporal de entrada
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_input:
            temp_input.write(generate_er_script(er_data))
            temp_input_path = temp_input.name
        
        # Archivo temporal de salida
        temp_output_path = "/tmp/diagram.svg"
        
        # Generar el diagrama
        render_er(temp_input_path, temp_output_path)
        
        # Leer y codificar el SVG
        with open(temp_output_path, "rb") as f:
            svg_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Limpiar archivos temporales
        os.remove(temp_input_path)
        os.remove(temp_output_path)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "image": f"data:image/svg+xml;base64,{svg_b64}",
                "format": "svg"
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Error al generar diagrama ER",
                "details": str(e),
                "traceback": traceback.format_exc()
            })
        }

def generate_er_script(data):
    """Genera el script de ERAlchemy a partir del JSON"""
    er_script = ""
    
    # Procesar entidades
    for entity in data.get('entities', []):
        er_script += f"{entity['name']} {{\n"
        for attr in entity.get('attributes', []):
            er_script += f"    {attr['name']} {attr['type']}"
            if attr.get('primary_key', False):
                er_script += " PK"
            if attr.get('nullable', True) is False:
                er_script += " NOT NULL"
            er_script += "\n"
        er_script += "}\n\n"
    
    # Procesar relaciones
    for relation in data.get('relations', []):
        left_card = relation.get('cardinality1', '')
        right_card = relation.get('cardinality2', '')
        er_script += f"{relation['entity1']} {left_card} -- {right_card} {relation['entity2']}\n"
    
    return er_script
