import argparse
import compileall
import os
import shutil
import re

def compile_and_copy(input_directory, output_directory):
    # Compile all .py files in the input directory
    compileall.compile_dir(input_directory, force=True)

    # Define the Python version suffix that you want to remove
    suffix = '.cpython-39'

    for foldername, subfolders, filenames in os.walk(input_directory):
        if '__pycache__' in foldername:
            for filename in filenames:
                if filename.endswith(suffix + '.pyc'):
                    old_filepath = os.path.join(foldername, filename)
                    new_filename = re.sub(suffix, '', filename)

                    # Create the same directory structure in the output directory
                    new_foldername = foldername.replace(input_directory, output_directory, 1)
                    new_foldername = new_foldername.rsplit('__pycache__', 1)[0]  # Remove the __pycache__
                    os.makedirs(new_foldername, exist_ok=True)

                    new_filepath = os.path.join(new_foldername, new_filename)

                    # Copy the file to the new location
                    shutil.copy2(old_filepath, new_filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile Python files and copy .pyc files to another directory.')
    parser.add_argument('input_directory', type=str, help='The directory to compile.')
    parser.add_argument('output_directory', type=str, help='The directory to copy the compiled files to.')
    args = parser.parse_args()

    # Call the function
    compile_and_copy(args.input_directory, args.output_directory)

