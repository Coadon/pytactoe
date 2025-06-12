import PyInstaller.__main__

PyInstaller.__main__.run([
    "-y",  # force clean.
    "--name=py-tac-toe",
    "--windowed",
    "--console",
    "--add-data=assets/*:assets",
    "pytactoe/main.py"
])
