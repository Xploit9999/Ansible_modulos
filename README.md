# Ansible_modulos

Repositorio dedicado a la creación de **módulos personalizados para Ansible**, con el objetivo de extender sus capacidades y permitir automatizaciones más específicas o de bajo nivel en sistemas Linux, Unix o Windows.

## 📦 Módulos disponibles

### 🔍 `get_pids`
Módulo para obtener los **PIDs (Process IDs)** de uno o varios procesos activos por su nombre.

- Útil para auditorías, chequeos de estado o validaciones previas a tareas de administración.
- Retorna una lista de PIDs que coinciden con el nombre del proceso especificado.

---

### 🛑 `kill`
Módulo para **finalizar procesos** por PID o por nombre.

- Permite detener procesos de forma selectiva.
- Compatible con señales de terminación personalizadas (ej. `SIGTERM`, `SIGKILL`).

---

### 📖 `leer_excel`
Módulo para la **lectura de archivos Excel** (`.xlsx`).

- Lee datos desde hojas y rangos definidos.
- Útil en flujos donde Ansible consume configuraciones o parámetros desde documentos externos.

---

### ✏️ `mod_excel`
Módulo para la **modificación de documentos Excel** (`.xlsx`).

- Permite la inserción de datos a un documento excel tomando de referencia un delimitador o un rango de celdas para su escritura.
- Ideal para generar reportes o registros automatizados en formato Excel.

---

### 🔐 `openssl_sig`
Módulo para **firmar contenido con OpenSSL**.

- Firma cadenas de texto o archivos usando claves privadas.
- Soporta los métodos `dgst` y `pkeyutl`.
- Retorna la firma en base64.
- Compatible con múltiples algoritmos de hashing (`sha256`, `sha512`, etc).

---

## 🔧 Requisitos

- Python 3.x
- Ansible
- Para los módulos relacionados con Excel:
  - `openpyxl` (instalable vía `pip install openpyxl`)
- Para `openssl_sig`:
  - OpenSSL disponible en el sistema (`openssl` CLI)
  - Claves privadas en formato PEM

---

## 🧑‍💻 Autor

[Xploit9999](https://github.com/Xploit9999) 
