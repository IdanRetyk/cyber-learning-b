import dis
import marshal

def decompile_pyc(file_path):
    """
    Decompile a Python .pyc file and disassemble its bytecode.
    """
    with open(file_path, "rb") as f:
        # Skip the .pyc header (first 16 bytes in Python 3.7+)
        f.read(16)
        code_object = marshal.load(f)

    # Disassemble the code object
    print("Disassembled Bytecode:")
    dis.dis(code_object)

    # Optionally, return the code object for further inspection
    return code_object


# Specify the path to your .pyc file
pyc_file = "path_to_your_pyc_file.pyc"  # Replace with your .pyc file path
code_obj = decompile_pyc(pyc_file)
