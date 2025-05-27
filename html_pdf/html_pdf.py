#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import asyncio
import os
from pyppeteer import launch

async def convertir_html_a_pdf(ruta_html, ruta_pdf, formato_hoja, orientacion):

    navegador = await launch()
    pagina = await navegador.newPage()
    await pagina.setViewport({'width': 1200, 'height': 800})

    url_archivo = 'file://' + os.path.abspath(ruta_html)
    await pagina.goto(url_archivo, waitUntil='load', timeout=0)
    await asyncio.sleep(1) 

    await pagina.pdf({
        'path': ruta_pdf,
        'format': formato_hoja,
        'landscape': orientacion == 'horizontal',
        'printBackground': True,
        'margin': {
            'top': '20px',
            'right': '20px',
            'bottom': '20px',
            'left': '20px'
        }
    })

    await navegador.close()

def main():

    modulo = AnsibleModule(
        argument_spec=dict(
            origen=dict(type='path', required=True),
            destino=dict(type='path', required=True),
            formato_hoja=dict(type='str', required=False, default='A4'),
            orientacion=dict(type='str', required=False, choices=['vertical', 'horizontal'], default='vertical')
        )
    )

    ruta_html = os.path.abspath(modulo.params['origen'])
    ruta_pdf = os.path.abspath(modulo.params['destino'])
    formato_hoja = modulo.params['formato_hoja']
    orientacion = modulo.params['orientacion']

    if not os.path.exists(ruta_html):
        modulo.fail_json(msg=f"El archivo HTML no existe en la ruta: {ruta_html}")

    try:
        asyncio.run(convertir_html_a_pdf(ruta_html, ruta_pdf, formato_hoja, orientacion))
        modulo.exit_json(changed=True, msg="PDF generado correctamente", destino=ruta_pdf)
    except Exception as error:
        modulo.fail_json(msg=f"Error al generar el PDF: {str(error)}")

if __name__ == '__main__':
    main()
