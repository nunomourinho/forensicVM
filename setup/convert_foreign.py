import sys

def convert_to_control_format(input_file):
    dependencies = []
    
    with open(input_file, 'r') as f:
        for line in f:
            # Split each line by spaces to extract package name, version, and distribution
            package_info = line.strip().split(' ')
            print(len(package_info))
            print(package_info[2])

            if len(package_info) == 4 and package_info[2] == 'Debian':
                package_name = package_info[0]
                package_version = package_info[1]
                distribution = package_info[3]
                
                # Format the dependency line in the Debian control format
                dependency_line = f"{package_name} (>= {package_version}) ({distribution})"
                dependencies.append(dependency_line)
    
    # Combine all the dependency lines into a single string
    control_format = ", ".join(dependencies)
    return control_format

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_control.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    control_format_result = convert_to_control_format(input_file_path)

    with open(output_file_path, 'w') as output_file:
        output_file.write("Generated debian/control format:\n")
        output_file.write(control_format_result)

    print(f"Result written to {output_file_path}.")

