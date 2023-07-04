import os
import inspect
import sys
import importlib.util
import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

# Initialize Django
django.setup()

def extract_functions_and_docstrings(directory):
    # Create a new directory to store the processed files
    output_directory = f"{directory}_output"
    os.makedirs(output_directory, exist_ok=True)

    # Process each file in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".py") and file_name != "admin.py":
            file_path = os.path.join(directory, file_name)
            output_file_name = os.path.splitext(file_name)[0] + "_docstring.py"
            output_file_path = os.path.join(output_directory, output_file_name)

            # Import the module dynamically
            module_name = os.path.splitext(file_path)[0].replace(os.sep, ".")
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get all members of the module
            members = inspect.getmembers(module)

            # Filter out functions and classes
            functions = []
            classes = []

            for name, member in members:
                if inspect.isfunction(member):
                    functions.append(member)
                elif inspect.isclass(member):
                    classes.append(member)

            # Write the extracted functions, classes, and their docstrings to the output file
            with open(output_file_path, 'w') as f:
                for function in functions:
                    # Write function definition
                    f.write(inspect.getsource(function))

                    # Write function docstring
                    docstring = inspect.getdoc(function)
                    if docstring:
                        f.write(f'    """{docstring}"""\n')

                    f.write('\n')

                for cls in classes:
                    # Write class definition
                    f.write(inspect.getsource(cls))

                    # Write class docstring
                    docstring = inspect.getdoc(cls)
                    if docstring:
                        f.write(f'    """{docstring}"""\n')

                    f.write('\n')

    print(f"Processed files saved in: {output_directory}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a directory name as an argument.")
    else:
        directory = sys.argv[1]
        extract_functions_and_docstrings(directory)

