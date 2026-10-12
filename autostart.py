import winreg
import sys
import os

def add_to_startup():
    # Настройка путей: python - обязательно с pythonw. Остальные параметры - абсолютные пути
    pythonw = r"C:\Users\korde\AppData\Local\Programs\Python\Python310\pythonw.exe"
    script_widget = os.path.abspath(r'D:\Programming\GitFut Widget\widget.py')
    script_parser = os.path.abspath(r'D:\Programming\GitFut Widget\gitfut_parser.py')
    image = os.path.abspath(r"D:\Programming\GitFut Widget\Kordebalet67-gitfut.png")
    
    # Команда для автозапуска
    command_1 = f'"{pythonw}" "{script_widget}" "{image}"'
    command_2 = f'"{pythonw}" "{script_parser}" "{image}"'
    
    # Путь в реестре для текущего пользователя
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "ImageWidget"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command_1)
        print(f"✓ Автозапуск добавлен: {command_1}")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command_2)
        print(f"✓ Автозапуск добавлен: {command_2}")
    except Exception as e:
        print(f"✗ Ошибка: {e}")

def remove_from_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "ImageWidget"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, name)
        print("✓ Автозапуск удалён")
    except FileNotFoundError:
        print("Автозапуск и так не был настроен")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--remove":
        remove_from_startup()
    else:
        add_to_startup()
    
    input("Нажмите Enter для выхода...")

# Если есть программы мониторинга автозапуска, то, при умпешном выполнении скрипта,
# сразу появится сообщение о новом элементе автозагрузки