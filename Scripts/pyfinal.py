import subprocess
import argparse
import hashlib
import datetime
import platform
import logging

# [ModulosPython]

# Modulos no usados actualmente
#from netfw_ps import menu_netfw as netfw
#import SHODAN_QUERY
#import passwords_management
#import Abuse_verif_menu
#import request

# [Definicion_Argumentos_Y_Opciones]

arguments = argparse.ArgumentParser()
arguments.add_argument("-f", "--file", help="Especifica el script principal o la tarea unificada a ejecutar. 'script_arocultos_urlhaus.py' escanea URLs o lista los arhivos ocultos en la carpeta actual.", type=str, choices=["Select-SecTask.ps1", "main_bash1.2.py", "main_menu.py", "script_arocultos_urlhaus.py"], default="")
arguments.add_argument("-o","--option", help="Especifica la tarea a ejecutar por medio de el identificador númerico de la tarea. IDENTIFICADORES_NUMERICOS: 'Select-SecTask.ps1': 1, 2, 3, 4 ; 'main_bash1.2.py': 1,2 ; 'main_menu.py': 1, 2, 3, 4, 5 ", type=int, default=0)
arguments.description = "DESCRIPCIÓN: Ejecuta una tarea especificada de el menu especificado o ejecuta el script unificado."
args = arguments.parse_args()

# Falta agregar el bloque de codigo para ejecutar una tarea que no se encuentre en los scripts principales
# python final_project-g2.py --file <script_name> --option <task_number> 

class glob_vars:
    # <global_variables>
    op_sys = platform.system()
    files = ["Select-SecTask.ps1", "main_bash1.2.py", "main_menu.py", "script_arocultos_urlhaus.py"]
    script_name = str(args.file)
    task_number = int(args.option)
    current_date = str(datetime.date.today())

    if (op_sys == "Windows"):
        try:
            # Ejecuta el siguiente comando, captura su salida en texto plano y guarda el valor de stdout de el comando a la variable output
            output = subprocess.run(f"ATTRIB /S \\{script_name}", capture_output=True, text=True).stdout
            # Divide la salida en tres partes a partir del separador
            div_output = output.partition("C:")
            # Obtiene los valores de la cadena en 1 (separador) y la cadena en 2 (ruta)
            unit_output = div_output[1]
            path_output = div_output[2]
            # Concatena estos dos valores anteriores
            script_path = unit_output + path_output

            if (len(script_path) == 0):
                script_path = f"Archivo {script_name} no encontrado."
        
        except KeyboardInterrupt:
            print("Ha interrumpido el programa.")

    elif (op_sys == "Linux"):
        try:
            script_path = subprocess.run(f"find / -name {script_name}", capture_output=True, text=True, shell=True).stdout
            
            if (len(script_path) == 0):
                script_path = f"Archivo {script_name} no encontrado."
        
        except KeyboardInterrupt:
            print("Ha interrumpido el programa.")

# [Funciones]

# Devuelve falso o verdadero dependiendo de si el argumento de interprete ingresado es PowerShell o no
def taskisps(file = glob_vars.script_name):
    if (glob_vars.files[0] == file or glob_vars.files[3] == file):
        return True
    else:
        return False

# Devuelve falso o verdadero dependiendo de si el argumento de interprete ingresado es Bash o no
def taskisbash(file = glob_vars.script_name):
    if (glob_vars.files[1] == file):
        return True
    else:
        return False

# Devuelve falso o verdadero dependiendo de si el argumento de interprete ingresado es Python o no
def taskispy(file = glob_vars.script_name):
    if (glob_vars.files[2] == file or glob_vars.files[4] == file):
        return True
    else:
        return False

# Generacion del mensaje de advertencia
def warning_mssg(op_sys = glob_vars.op_sys):
    if (op_sys == "Windows" and taskisbash()):
        logging.warning("\tEsta tarea de bash no es soportada por Windows.")
        warn_mssg = "ADVERTENCIA: Esta tarea de bash no es soportada por Windows."

    elif (op_sys == "Linux" and taskisps()):
        logging.warning("\tEsta tarea de powershell no es soportada por un sistema Linux.")
        warn_mssg = "ADVERTENCIA: Esta tarea de powershell no es soportada por un sistema Linux."
    
    else:
        warn_mssg = None

    return warn_mssg

# Generacion del mensaje de error
def error_mssg(task_number = glob_vars.task_number):
    script_name = glob_vars.script_name

    if (script_name == "Select-SecTask.ps1"):
        if (task_number > 4 or task_number < 1):
            str(logging.error("\tLa tarea es desconocida."))
            err_mssg = "ERROR: La tarea es desconocida"
        else:
            err_mssg = None

    elif (script_name == "main_bash1.2.py"):
        if (task_number > 2 or task_number < 1):
            
            logging.error("\tLa tarea es desconocida.")
            err_mssg = "ERROR: La tarea es desconocida"
        else:
            err_mssg = None

    elif (script_name == "main_menu.py"):
        if (task_number > 5 or task_number < 1):
            logging.error("\tLa tarea es desconocida.")
            err_mssg = "ERROR: La tarea es desconocida"
        else:
            err_mssg = None
    
    return err_mssg

# Generación de reportes individuales en base al nombre del script \ 
# y el argumento numerico que identifica la tarea a ejecutar
def mk_report(task_number = glob_vars.task_number, script_name = glob_vars.script_name):
    current_date = glob_vars.current_date

    # Escritura de el numero de tarea (identificador de tarea), la fecha en la que se ejecuto (hoy) \
    # el nombre del script necesario para ejecutar la tarea y la ruta del mismo
    if (script_name == "script_arocultos_urlhaus.py"):
        report = open(f"{script_name}_report.txt", "a")
        report.writelines([f"\nFecha: {current_date}\n", f"Nombre: {script_name}\n", f"Ruta: {glob_vars.script_path}\n"])
        report.close()

    else:
        if (task_number == 0):
            # El valor predeterminado de task_number es 0 por lo que si no es especificado, este sera el valor guardado en task_number
            report = open(f"{script_name}_report.txt", "a")
            report.writelines("\nFalta de argumento en el parametro --option.")
            report.close()
        
        elif (task_number >= 1 and task_number <= 5):
            report = open(f"task-{str(task_number)}_report.txt", "a")
            report.writelines([f"\nTarea: {str(task_number)}\n", f"Fecha: {current_date}\n", f"Nombre: {script_name}\n", f"Ruta: {glob_vars.script_path}"])
            # Si el valor que tiene task_number no es un identificador de tarea numerico valido para el script en script_name
            err_mssg = error_mssg()

            if (err_mssg != None):
                report.writelines(f"\n{err_mssg}")

            report.close()
        
        elif ((task_number > 5 or task_number < 1) and task_number != 0):
            # Si la tarea tarea es menor que 1 o mayor que 5, y excluyendo al valor 0
            report = open(f"{script_name}_report.txt", "a")
            err_mssg = error_mssg()
            report.writelines([f"\nFecha: {current_date}\n", f"Nombre: {script_name}\n", f"Ruta: {glob_vars.script_path}", f"{err_mssg}\n"])
            report.close()

    return report

# Generacion de hash de el reporte individual resultante
def hash_file():
    report = mk_report()
    bin_report = open(report.name, "rb")
    buff_report = bin_report.read()
    file_hash = hashlib.sha256()
    file_hash.update(buff_report)
    file_hash = file_hash.hexdigest().upper()
    bin_report.close()

    return file_hash

# Generacion de el reporte final
def end_report():
    end_report = open("end_report.txt", "a+")

    report = mk_report()    
    file_hash = hash_file()

    read_report = open(report.name, "r")
    read = read_report.read()
    # Obtencion del contenido escrito en texto plano (no binario)
    read_report.close()

    end_report.writelines([f"\n{read}", f"Hash: {file_hash}"])
    
    warn_msg = warning_mssg()
    if (warn_msg != None):
        end_report.writelines(f"\n{warn_msg}")
    
    end_report.close()

# Ejecucion del script principal, dependiendo de el nombre del script ingresado
def run_script(script_name = glob_vars.script_name):
    op_sys = glob_vars.op_sys

    try:
        script_path = glob_vars.script_path

        if (op_sys == "Windows" and taskisps()):
            cmdline = subprocess.run(f"Powershell -ExecutionPolicy ByPass -Command {script_path}", errors=None, capture_output=True)
            mk_report()
            file_hash = hash_file()
            print(f"\nTAREA:  {glob_vars.task_number}")
            print(f"FECHA:  {glob_vars.current_date}")
            print(f"SCRIPT: {script_name}")
            print(f"RUTA:   {script_path}")
            print(f"HASH:   {file_hash}\n")
            end_report()

        elif (op_sys == "Windows" and taskisbash()):
            mk_report()
            file_hash = hash_file()
            print(f"\nTAREA:  {glob_vars.task_number}")
            print(f"FECHA:  {glob_vars.current_date}")
            print(f"SCRIPT: {script_name}")
            print(f"RUTA:   {script_path}")
            print(f"HASH:   {file_hash}\n")
            end_report()

        elif (op_sys == "Linux" and taskisbash()):
            cmdline = subprocess.run(f"Bash {script_path}", shell=True, errors=None, capture_output=True)
            mk_report()
            file_hash = hash_file()
            print(f"\nTAREA:  {glob_vars.task_number}")
            print(f"FECHA:  {glob_vars.current_date}")
            print(f"SCRIPT: {script_name}")
            print(f"RUTA:   {script_path}")
            print(f"HASH:   {file_hash}\n")
            end_report()

        elif (op_sys == "Linux" and taskisps()):
            mk_report()
            file_hash = hash_file()
            print(f"\nTAREA:  {glob_vars.task_number}")
            print(f"FECHA:  {glob_vars.current_date}")
            print(f"SCRIPT: {script_name}")
            print(f"RUTA:   {script_path}")
            print(f"HASH:   {file_hash}\n")
            end_report()

        elif ([op_sys == "Windows" or op_sys == "Linux"] and taskispy()):
            div_path = script_path.partition(f"{script_name}")
            cwd = div_path[0]
            cmdline = subprocess.run(f"python {script_path}", errors=None, cwd=cwd, capture_output=True)
            mk_report()
            file_hash = hash_file()
            print(f"\nTAREA:  {glob_vars.task_number}")
            print(f"FECHA:  {glob_vars.current_date}")
            print(f"SCRIPT: {script_name}")
            print(f"RUTA:   {script_path}")
            print(f"HASH:   {file_hash}\n")
            end_report()

        else:
            print("El sistema que esta usando actualmente no es compatible o la tarea es desconocida.")
            # op_sys es cualquier sistema que no sea Windows o Linux. \ 
            # Independientemente de que lenguaje se ejecute la tarea.
        
        exit()

    except KeyboardInterrupt:
        print("\nHa interrumpido el programa.")
        exit()

    except subprocess.CalledProcessError:
        print("Ocurrio un error. Verifique que tenga instalados los scripts necesarios.")
        exit()
    
    except AttributeError:
        print("")
        exit()

# [Ejecucion]

# Dado que el valor predeterminado de la longitud de el argumento ingresado en el parametro --file es cero, \ 
# entonces este script no se ejecutara a menos que se especifique un script en el agumento de el parametro --file
if (len(glob_vars.script_name) != 0):
    try:
        #request.main
        run_script()

    except KeyboardInterrupt:
        print("\nHa interrumpido el programa.")
        exit()

else:
    # Muestra la ayuda del comando en la terminal si no se han ingresado los parametros
    arguments.print_help()