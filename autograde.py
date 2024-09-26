import subprocess
import argparse
from os import path, remove


def gen_file_path(num, i, form):
    return f"tc_hw{num}/tc{i:02}." + form


def check_process_result(result):
    if result.returncode != 0:
        raise RuntimeError(result)


def main():
    # Correctness flag
    f_correct = 0

    # Parse arguments from the user
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of file")
    parser.add_argument("-hw", "--homework", help="Homework Number")
    parser.add_argument("-c", "--compile", help="Name of the executable")

    args = parser.parse_args()

    # Define arguments in variable
    program_name = args.name
    exe_name = args.compile
    homework_num = args.homework

    # Compile the c file
    result = subprocess.run(f"g++ {program_name} -o {exe_name}")
    check_process_result(result)

    # Run every test case
    i = 1
    input_path = gen_file_path(homework_num, i, "in")
    output_path = gen_file_path(homework_num, i, "out")
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
            f_correct -= 1
            print(result)

        i += 1
        input_path = gen_file_path(homework_num, i, "in")
        output_path = gen_file_path(homework_num, i, "out")

        if f_correct >= 0:
            print("All correct 100%")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(e)
        print("Incorrect usage, must contain flags [-n  | name of your c file] \n" +
              "                                    [-hw | the homework number] \n" +
              "                                    [-c  | the desired name of the executable]")
