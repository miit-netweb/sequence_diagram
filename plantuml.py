import subprocess
import os
from pathlib import Path

def run_plantuml_jar(puml_file_path, jar_file_path="plantuml.1.2023.7.jar"):

    puml_file_path = Path(puml_file_path)
    jar_file_path = Path(jar_file_path)

    if not puml_file_path.exists():
        raise FileNotFoundError(f"PlantUML file not found: {puml_file_path}")

    if not jar_file_path.exists():
        raise FileNotFoundError(f"PlantUML JAR file not found: {jar_file_path}")

    try:
        command = ["java", "-jar", str(jar_file_path), str(puml_file_path)]
        subprocess.run(command, check=True, capture_output=True, text=True) #capture output for error checking.
        print(f"Successfully processed {puml_file_path} using {jar_file_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing {puml_file_path}:")
        print(e.stderr)
        raise #re raise the exception to stop the program.
    except FileNotFoundError:
        print("Java or PlantUML not found. Please ensure they are installed and in your PATH.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
