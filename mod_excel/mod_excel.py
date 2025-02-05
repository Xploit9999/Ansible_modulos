#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Módulo de Ansible: mod_excel

Este módulo permite modificar archivos de Excel en formato `.xlsx`, reemplazando un delimitador en una celda con datos específicos 
y escribiendo los datos horizontalmente en la misma fila. Posteriormente, el delimitador se coloca en la siguiente fila.

## Parámetros

- `ruta` (str, requerido): Ruta del archivo de Excel a modificar.
- `hoja` (str, opcional): Nombre de la hoja de cálculo donde se realizará la modificación. Si no se especifica, se usará la hoja activa.
- `delimitador` (str, requerido): Texto delimitador que se usará como referencia para escribir los datos.
- `data` (list, requerido): Lista de valores que serán escritos en la hoja de cálculo.

## Funcionamiento

1. Se busca el `delimitador` en la hoja de cálculo.
2. Se sobrescribe el delimitador con el primer dato de la lista.
3. Se escriben los datos en la fila encontrada, en distintas columnas (horizontalmente).
4. El delimitador se coloca en la siguiente fila, en la misma columna donde fue encontrado.

## Notas

- Si el `delimitador` no se encuentra en la hoja de cálculo, el módulo fallará.
- Se recomienda hacer una copia de seguridad del archivo antes de ejecutar el módulo, ya que modifica directamente el archivo original.
- El módulo debe ejecutarse en un entorno donde `openpyxl` esté disponible.

## Ejemplo de uso en Ansible

```yaml
- name: Modificar archivo Excel con datos y delimitador
  hosts: localhost
  tasks:
    - name: Modificar Excel
      mod_excel:
        ruta: "/ruta/al/archivo.xlsx"
        hoja: "Formulario"
        delimitador: "*/"
        data:
          - "Valor 1"
          - "Valor 2"
          - "Valor 3"

## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)
"""

from ansible.module_utils.basic import AnsibleModule
import openpyxl

def busca_delimitador(sheet, delimitador):

    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == delimitador:
                return cell
    return None

def modificar_excel(modulo):
    ruta = modulo.params['ruta']
    hoja = modulo.params.get('hoja')
    delimitador = modulo.params['delimitador']
    data = modulo.params['data']

    try:
        workbook = openpyxl.load_workbook(ruta)
        
        if hoja:
            sheet = workbook[hoja]
        else:
            sheet = workbook.active

        delimitador_final = busca_delimitador(sheet, delimitador)
        if not delimitador_final:
            modulo.fail_json(msg=f"Delimitador '{delimitador}' no encontrado en la hoja.")

        column = delimitador_final.column_letter  
        row = delimitador_final.row              

        sheet[f"{column}{row}"] = None

        for index, item in enumerate(data):
            next_column = chr(ord(column) + index)  
            sheet[f"{next_column}{row}"] = item

        sheet[f"{column}{row + 1}"] = delimitador

        workbook.save(ruta)

        modulo.exit_json(changed=True, msg="El archivo se ha modificado satisfactoriamente!")
    except Exception as e:
        modulo.fail_json(msg=f"Falla al momento de modificar el archivo: {str(e)}")

def iniciar_proceso():
    argumentos = dict(
        ruta=dict(type='str', required=True),
        hoja=dict(type='str', required=False),
        delimitador=dict(type='str', required=True),
        data=dict(type='list', required=True)
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
