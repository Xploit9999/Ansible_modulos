#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Módulo de Ansible: mod_excel

Este módulo permite modificar archivos de Excel en formato `.xlsx`, escribiendo datos horizontalmente a partir de una celda inicial.
El módulo también permite reemplazar un delimitador en una celda con datos específicos y mover dicho delimitador a la siguiente fila.

## Parámetros

- `ruta` (str, requerido): Ruta del archivo de Excel a modificar.
- `hoja` (str, opcional): Nombre de la hoja de cálculo donde se realizará la modificación. Si no se especifica, se usará la hoja activa.
- `data` (list, requerido): Lista de listas que contiene los valores a escribir. Cada sublista representa una fila.
- `delimitador` (str, opcional): Texto delimitador que se usará como referencia para escribir los datos. Si se proporciona, `celda_inicial` y `celda_final` no son necesarios.
- `celda_inicial` (str, opcional): Celda de inicio para escribir los datos. Requiere `celda_final`.
- `celda_final` (str, opcional): Celda final del rango donde se escribirán los datos. Requiere `celda_inicial`.

## Funcionamiento

### Si se utiliza el delimitador:
1. Se busca el `delimitador` en la hoja.
2. Se reemplaza el delimitador con los datos proporcionados, en la fila y columna donde se encontró.
3. Se escriben los datos horizontalmente en la misma fila.
4. El `delimitador` se mueve a la fila siguiente, en la misma columna.

### Si se utilizan `celda_inicial` y `celda_final`:
1. Se calcula el rango definido por ambas celdas.
2. Se escriben los datos proporcionados dentro de ese rango.

## Notas

- Si no se encuentra el `delimitador`, el módulo fallará.
- Si se usan `celda_inicial` y `celda_final`, se ignora el `delimitador`.
- El módulo requiere que `openpyxl` esté instalado en el entorno Python de ejecución.
- Se recomienda respaldar el archivo antes de modificarlo.

## Ejemplo de uso con delimitador

```yaml
- name: Modificar Excel
  mod_excel:
    ruta: "/ruta/al/archivo.xlsx"
    hoja: "Formulario"
    delimitador: "*/"
    data:
      - "Valor 1"
      - "Valor 2"
      - "Valor 3"

- name: Escribir una fila en el siguiente espacio vacío del rango
  mod_excel:
    ruta: "/ruta/archivo.xlsx"
    celda_inicial: "A34"
    celda_final: "J34"
    data:
      - ["dato1", "dato2", "dato3"]

- name: Escribir varias filas en el siguiente espacio vacío del rango
  mod_excel:
    ruta: "/ruta/archivo.xlsx"
    celda_inicial: "A34"
    celda_final: "J37"
    data:
      - ["dato1", "dato2", "dato3"]
      - ["dato4", "dato5", "dato6"]
      - ["dato7", "dato8", "dato9"]
```yaml
"""
import openpyxl
from ansible.module_utils.basic import AnsibleModule

def busca_delimitador(sheet, delimitador):
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == delimitador:
                return cell
    return None

def celda_a_fila_columna(celda):
    col = ord(celda[0].upper()) - ord('A') + 1
    row = int(celda[1:])
    return row, col

def es_fila_vacia(sheet, fila, col_inicio, col_fin):
    for col in range(col_inicio, col_fin + 1):
        if sheet.cell(row=fila, column=col).value not in [None, ""]:
            return False
    return True

def escribir_datos_en_rango(sheet, celda_inicial, celda_final, data):
    fila_ini, col_ini = celda_a_fila_columna(celda_inicial)
    fila_fin, col_fin = celda_a_fila_columna(celda_final)
    
    datos_escritos = 0

    for fila in range(fila_ini, fila_fin + 1):
        if datos_escritos >= len(data):
            break

        if es_fila_vacia(sheet, fila, col_ini, col_fin):
            for offset, value in enumerate(data[datos_escritos]):
                col_actual = col_ini + offset
                if col_actual <= col_fin:
                    sheet.cell(row=fila, column=col_actual).value = value
            datos_escritos += 1

    return datos_escritos

def modificar_excel(modulo):
    ruta = modulo.params['ruta']
    hoja = modulo.params.get('hoja')
    delimitador = modulo.params.get('delimitador')
    data = modulo.params['data']
    celda_inicial = modulo.params.get('celda_inicial')
    celda_final = modulo.params.get('celda_final')

    if delimitador and (celda_inicial or celda_final):
        modulo.fail_json(msg="No se puede usar 'delimitador' con 'celda_inicial' o 'celda_final'.")

    try:
        workbook = openpyxl.load_workbook(ruta)
        sheet = workbook[hoja] if hoja else workbook.active

        if delimitador:
            celda = busca_delimitador(sheet, delimitador)
            if not celda:
                modulo.fail_json(msg=f"Delimitador '{delimitador}' no encontrado.")

            col = celda.column
            row = celda.row

            sheet.cell(row=row, column=col).value = None

            for i, val in enumerate(data):
                sheet.cell(row=row, column=col + i).value = val

            sheet.cell(row=row + 1, column=col).value = delimitador

        else:
            if not celda_inicial or not celda_final:
                modulo.fail_json(msg="Debe especificar 'celda_inicial' y 'celda_final' si no se usa 'delimitador'.")

            if not isinstance(data[0], list):
                data = [data]  

            filas_escritas = escribir_datos_en_rango(sheet, celda_inicial, celda_final, data)
            if filas_escritas == 0:
                modulo.fail_json(msg="No se encontraron filas vacías en el rango para escribir datos.")

        workbook.save(ruta)
        modulo.exit_json(changed=True, msg="El archivo se modificó correctamente.")

    except Exception as e:
        modulo.fail_json(msg=str(e))

def iniciar_proceso():
    argumentos = dict(
        ruta=dict(type='str', required=True),
        hoja=dict(type='str', required=False),
        delimitador=dict(type='str', required=False, default=None),
        data=dict(type='list', required=True),
        celda_inicial=dict(type='str', required=False, default=None),
        celda_final=dict(type='str', required=False, default=None)
    )

    modulo = AnsibleModule(
        argument_spec=argumentos,
        supports_check_mode=True
    )

    if modulo.check_mode:
        modulo.exit_json(changed=False)

    modificar_excel(modulo)

if __name__ == '__main__':
    iniciar_proceso()
