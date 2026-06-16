import os
import sys
import importlib
import traceback

def main():
    root = "."
    sys.path.insert(0, os.path.abspath(root))
    errors = []
    
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith(".py") and file != "check_imports.py" and "venv" not in dirpath and "__pycache__" not in dirpath:
                rel_path = os.path.relpath(os.path.join(dirpath, file), root)
                module_name = rel_path.replace(os.sep, ".")[:-3]
                if module_name.endswith(".__init__"):
                    module_name = module_name[:-9]
                
                try:
                    importlib.import_module(module_name)
                except Exception as e:
                    errors.append((module_name, str(e)))
                    
    if errors:
        print(f"Found {len(errors)} import errors:")
        for mod, err in errors:
            print(f"{mod}: {err}")
        sys.exit(1)
    else:
        print("All imports successful.")
        sys.exit(0)

if __name__ == "__main__":
    main()
