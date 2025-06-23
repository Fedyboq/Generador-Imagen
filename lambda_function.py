import os
import tempfile
import json
from eralchemy2 import render_er

def handler(event, context):
    try:
        os.environ['PATH'] += os.pathsep + '/usr/bin'
        body = json.loads(event.get('body', '{}'))
        schema_definition = body.get('schema', '')
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            output_path = tmp_file.name
        render_er(schema_definition, output_path)
        with open(output_path, 'rb') as f:
            image_data = f.read()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Access-Control-Allow-Origin': '*'
            },
            'body': image_data.hex(),
            'isBase64Encoded': True
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

