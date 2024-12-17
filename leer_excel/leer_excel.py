import openpyxl
from ansible.module_utils.basic import AnsibleModule

def leer_excel(ruta, hoja_nombre, celda_inicial, num_columnas, delimitador=None, celda_final=None):
    # Verificar exclusión mutua entre delimitador y celda_final
    if delimitador and celda_final:
        raise ValueError("No se puede usar 'delimitador' y 'celda_final' juntos.")
    if not delimitador and not celda_final:
        raise ValueError("Debe especificarse 'delimitador' o 'celda_final'.")

    # Obtener columna y fila de la celda_inicial
    columna_inicial = ord(celda_inicial[0].upper()) - ord('A') + 1
    fila_inicial = int(celda_inicial[1:])

    # Si se especifica celda_final, obtener columna y fila de la celda final
    if celda_final:
        columna_final = ord(celda_final[0].upper()) - ord('A') + 1
        fila_final = int(celda_final[1:])
        max_col = columna_final  # Usar columna final
    else:
        # Si no se especifica celda_final, usar el número de columnas proporcionado
        max_col = columna_inicial + num_columnas - 1
        fila_final = fila_inicial + 1000  # Leer hasta la fila 1000 por defecto

    # Cargar el archivo Excel
    wb = openpyxl.load_workbook(ruta, data_only=True)
    hoja = wb[hoja_nombre]
    datos = []

    # Iterar sobre todas las filas hasta la fila_final
    for fila in hoja.iter_rows(min_row=fila_inicial, max_row=fila_final, min_col=columna_inicial, max_col=max_col):
        # Asegurarse de que cada celda se convierte a cadena y eliminamos espacios extra
        datos_fila = [str(celda.value).strip() if celda.value is not None else "" for celda in fila]

        # Verificar si el delimitador está presente en alguna de las celdas de la fila
        if delimitador and any(delimitador.strip() == valor for valor in datos_fila):  # Usar strip() para evitar errores con espacios
            break  # Detener la lectura al encontrar el delimitador

        datos.append(datos_fila)

    return datos

def run_module():
    module_args = dict(
        ruta=dict(type='str', required=True),
        hoja=dict(type='str', required=True),
        celda_inicial=dict(type='str', required=True),
        num_columnas=dict(type='int', required=True),
        delimitador=dict(type='str', required=False, default=None),
        celda_final=dict(type='str', required=False, default=None)
    )

    result = dict(
        changed=False,
        datos=None
    )

    try:
        # Inicializar el módulo
        module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

        # Obtener los datos del Excel
        result['datos'] = leer_excel(
            module.params['ruta'],
            module.params['hoja'],
            module.params['celda_inicial'],
            module.params['num_columnas'],
            module.params.get('delimitador'),
            module.params.get('celda_final')
        )

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    run_module()

