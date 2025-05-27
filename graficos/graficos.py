#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import plotly.express as px
import base64
import os

def codificar_base64(ruta):
    with open(ruta, 'rb') as imagen:
        return base64.b64encode(imagen.read()).decode('utf-8')

def procesar_datos(datos):
    etiquetas = []
    cantidades = []
    colores = []

    for etiqueta, info in datos.items():
        if isinstance(info, dict):
            cantidad = info.get('cantidad', 0)
            color = info.get('color')
        else:
            cantidad = info
            color = None

        etiquetas.append(etiqueta)
        cantidades.append(cantidad)
        colores.append(color)

    return etiquetas, cantidades, colores

def main():

    modulo = AnsibleModule(
        argument_spec=dict(
            distribucion=dict(type='dict', required=True),
            titulo_torta=dict(type='str', required=False, default='Gráfico de Distribución'),
            recurrencias=dict(type='dict', required=False, default={}),
            titulo_barras=dict(type='str', required=False, default='Gráfico de Medición'),
            carpeta_salida=dict(type='str', required=False, default='.'),
            incluir_base64=dict(type='bool', required=False, default=False),
        ),
        supports_check_mode=False
    )

    distribucion = modulo.params['distribucion']
    titulo_torta = modulo.params['titulo_torta']
    recurrencias = modulo.params['recurrencias']
    titulo_barras = modulo.params['titulo_barras']
    carpeta_salida = modulo.params['carpeta_salida']
    incluir_base64 = modulo.params['incluir_base64']

    try:
        etiquetas_torta, cantidades_torta, colores_torta = procesar_datos(distribucion)
        etiquetas_con_valores = [f"{etiqueta} ({cantidad})" for etiqueta, cantidad in zip(etiquetas_torta, cantidades_torta)]

        datos_pie = {
            'Etiqueta': etiquetas_con_valores,
            'Cantidad': cantidades_torta
        }

        figura_pie = px.pie(
            datos_pie,
            names='Etiqueta',
            values='Cantidad',
            title=titulo_torta,
        )

        if any(colores_torta):
            color_map = {label: color for label, color in zip(etiquetas_con_valores, colores_torta) if color}
            figura_pie.update_traces(marker=dict(colors=[color_map.get(lbl) for lbl in etiquetas_con_valores]))

        figura_pie.update_traces(textposition='inside', textinfo='percent+label')
        ruta_pie = os.path.join(carpeta_salida, "grafico_torta.png")
        figura_pie.write_image(ruta_pie, width=400, height=400)

        leyenda_barras = []

        if recurrencias:
            etiquetas_barras, cantidades_barras, colores_barras = procesar_datos(recurrencias)

            datos_barras = list(zip(etiquetas_barras, cantidades_barras, colores_barras))
            datos_barras.sort(key=lambda x: x[1], reverse=True)
            etiquetas_barras, cantidades_barras, colores_barras = zip(*datos_barras)

            figura_barras = px.bar(
                x=cantidades_barras,
                y=etiquetas_barras,
                title=titulo_barras,
                labels={'x': 'Cantidad', 'y': 'Tarea'},
                orientation='h'
            )
            figura_barras.update_layout(yaxis=dict(autorange="reversed"))

            figura_barras.update_traces(marker_color=[
                color if color else '#C9190B' for color in colores_barras
            ], text=cantidades_barras, textposition='outside')

            alto = max(400, len(etiquetas_barras) * 40)
            ruta_barras = os.path.join(carpeta_salida, "grafico_barras.png")
            figura_barras.write_image(ruta_barras, width=600, height=alto)

            leyenda_barras = [
                {"tarea": etiqueta, "cantidad": cantidad}
                for etiqueta, cantidad in zip(etiquetas_barras, cantidades_barras)
            ]
        else:
            ruta_barras = None

        resultado = {
            'changed': True,
            'grafico_torta': ruta_pie,
            'grafico_barras': ruta_barras,
            'leyenda_barras': leyenda_barras,
            'msg': "Gráficos generados correctamente"
        }

        if incluir_base64:
            resultado['grafico_torta_base64'] = codificar_base64(ruta_pie)
            if ruta_barras:
                resultado['grafico_barras_base64'] = codificar_base64(ruta_barras)

        modulo.exit_json(**resultado)

    except Exception as e:
        modulo.fail_json(msg=f"Error generando gráficos: {e}")

if __name__ == '__main__':
    main()
