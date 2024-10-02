import subprocess
import argparse
from os import path, remove


def gen_file_path(name, i, form):
    return f"{name}/tc{i:02}." + form


def check_process_result(result):
    if result.returncode != 0:
        raise RuntimeError(result)


def main():
    # Parse arguments from the user
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of file")
    parser.add_argument("-t", "--testcase", help="Test case Directory")
    parser.add_argument("-c", "--compile", help="Name of the executable")

    args = parser.parse_args()

    # Define arguments in variable
    program_name = args.name
    exe_name = args.compile
    tc_directory = args.testcase

    # Compile the c file
    result = subprocess.run(f"g++ {program_name} -o {exe_name}")
    check_process_result(result)

    # Run every test case
    i = 1
    input_path = gen_file_path(tc_directory, i, "in")
    output_path = gen_file_path(tc_directory, i, "out")
    while path.exists(input_path):
        print(f"Running {program_name} < {input_path}...")

        # Check if program works for test case
        subprocess.run(f"{exe_name} < {input_path} > run.out", shell=True)
        result = subprocess.run(f"fc run.out {output_path}", stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True).stdout
        # check_process_result(result)

        # Remove temporary file
        remove("run.out")

        # Only output a result if it deviates from the output
        if "FC: no differences encountered" not in result:
            print(result)
        else:
            print("Correct!")

        i += 1
        input_path = gen_file_path(tc_directory, i, "in")
        output_path = gen_file_path(tc_directory, i, "out")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(e)
        print("Incorrect usage, must contain flags [-n  | name of your c file] \n" +
              "                                    [-t | the test case directory] \n" +
              "                                    [-c  | the desired name of the executable]")
