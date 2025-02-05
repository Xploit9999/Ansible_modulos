# Módulo Ansible: `mod_excel`

Este módulo permite modificar documentos de Excel (`.xlsx`) identificando un delimitador en la hoja de cálculo y escribiendo datos a partir de esa posición.

## Requisitos

- Ansible
- Python 3.x
- `openpyxl` (instalable con `pip install openpyxl`)

## Parámetros

| Parámetro    | Tipo   | Requerido | Descripción                                                                    |
|--------------|--------|-----------|--------------------------------------------------------------------------------|
| `ruta`       | `str`  | Sí        | Ruta del archivo Excel a modificar.                                            |
| `hoja`       | `str`  | No        | Nombre de la hoja de cálculo. Si no se especifica, se usa la hoja activa.      |
| `delimitador`| `str`  | Sí        | Texto que indica el punto de inicio de la escritura y se coloca al final.      |
| `data`       | `list` | Sí        | Lista de datos que se escribirán en la fila donde se encuentra el delimitador. |

## Uso

Ejemplo de un playbook que usa el módulo:

```yaml
- name: Modificar archivo Excel con delimitador
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:

    - name: Modificar Excel con `mod_excel`
      mod_excel:
        ruta: "test.xlsx"
        hoja: "Hoja1"
        delimitador: "*/"
        data: 
          - "Valor 1"
          - "Valor 2"
          - "Valor 3"
```

## Funcionamiento

1. Se busca el `delimitador` en la hoja de cálculo.
2. Se sobrescribe el delimitador con el primer dato de la lista.
3. Se escriben los datos en la fila encontrada, en distintas columnas (horizontalmente).
4. El delimitador se coloca en la siguiente fila, en la misma columna donde fue encontrado.

## Notas

- Si el `delimitador` no se encuentra en la hoja de cálculo, el módulo fallará.
- Se recomienda hacer una copia de seguridad del archivo antes de ejecutar el módulo, ya que modifica directamente el archivo original.
- El módulo debe ejecutarse en un entorno donde `openpyxl` esté disponible.

## Author

- **John Freidman** - [@Xploit9999](https://github.com/Xploit9999)
