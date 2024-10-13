import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def main():
    print("Running security checks...")

    checks = [
        ("Bandit", "bandit -r project_initializer -f custom"),
        ("Safety", "safety check -r requirements.txt"),
        ("Pip-audit", "pip-audit"),
    ]

    exit_code = 0

    for check_name, command in checks:
        print(f"\nRunning {check_name}...")
        return_code, stdout, stderr = run_command(command)
        
        if return_code != 0:
            print(f"{check_name} found issues:")
            print(stdout.decode())
            print(stderr.decode())
            exit_code = 1
        else:
            print(f"{check_name} passed.")

    if exit_code == 0:
        print("\nAll security checks passed!")
    else:
        print("\nSome security checks failed. Please review the output above.")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
