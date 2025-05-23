#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import plotly.express as px
import base64
import os

def codificar_base64(ruta):
    with open(ruta, 'rb') as imagen:
        return base64.b64encode(imagen.read()).decode('utf-8')

def main():
    modulo = AnsibleModule(
        argument_spec=dict(
            exitos=dict(type='int', required=True),
            fallos=dict(type='int', required=True),
            recurrencias=dict(type='dict', required=False, default={}),
            carpeta_salida=dict(type='str', required=False, default='.'),
            incluir_base64=dict(type='bool', required=False, default=False),
        ),
        supports_check_mode=False
    )

    exitos = modulo.params['exitos']
    fallos = modulo.params['fallos']
    recurrencias = modulo.params['recurrencias']
    carpeta_salida = modulo.params['carpeta_salida']
    incluir_base64 = modulo.params['incluir_base64']

    try:
        datos_pie = {
            'Etiqueta': ['Éxitos', 'Fallos'],
            'Cantidad': [exitos, fallos]
        }

        figura_pie = px.pie(
            datos_pie, names='Etiqueta', values='Cantidad',
            title='Éxito vs Fallos',
            color='Etiqueta',
            color_discrete_map={'Éxitos': '#27AE60', 'Fallos': '#EE0000'}
        )
        figura_pie.update_traces(textposition='inside', textinfo='percent+label')
        ruta_pie = os.path.join(carpeta_salida, "grafico_torta.png")
        figura_pie.write_image(ruta_pie, width=400, height=400)

        etiquetas = list(recurrencias.keys())
        cantidades = list(recurrencias.values())

        figura_barras = px.bar(
            x=etiquetas, y=cantidades,
            title='Fallas Recurrentes',
            labels={'x': 'Tarea', 'y': 'Cantidad'},
            color_discrete_sequence=['#C9190B']
        )
        figura_barras.update_layout(xaxis_tickangle=-25, margin=dict(l=20, r=20, t=40, b=80))
        ruta_barras = os.path.join(carpeta_salida, "grafico_barras.png")
        figura_barras.write_image(ruta_barras, width=600, height=400)

        resultado = {
            'changed': True,
            'grafico_torta': ruta_pie,
            'grafico_barras': ruta_barras,
            'msg': "Gráficos generados correctamente"
        }

        if incluir_base64:
            resultado['grafico_torta_base64'] = codificar_base64(ruta_pie)
            resultado['grafico_barras_base64'] = codificar_base64(ruta_barras)

        modulo.exit_json(**resultado)

    except Exception as e:
        modulo.fail_json(msg=f"Error generando gráficos: {e}")

if __name__ == '__main__':
    main()
