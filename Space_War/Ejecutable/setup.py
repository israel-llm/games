import cx_Freeze
executables = [cx_Freeze.Executable("Juego2.py")]

cx_Freeze.setup(
    name = "Space War",
    options = {"build_exe":{"packages":["pygame"]}},
    description = "Juego del Espacio",
    executables = executables
    )
