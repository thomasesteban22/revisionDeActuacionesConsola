import os
import pyinstaller


# Nombre de tu script
script_name = "tu_script.py"

# Compilar el script a un ejecutable
pyinstaller.run([
    "--onefile",
    "--noconsole",
    script_name
])

# Ruta del archivo ejecutable
exe_path = os.path.join("dist", f"{script_name}.exe")

# Crear acceso directo en el escritorio
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
shortcut_path = os.path.join(desktop_path, f"{script_name}.lnk")

with open(shortcut_path, "w") as f:
    f.write(f"""[Desktop Entry]
Type=Application
Name={script_name}
Exec={exe_path}
Icon={exe_path}
Comment={script_name}
Categories=Application;
""")

print("¡.exe and direct acces created!")
