from subprocess import Popen, PIPE
from pandas import DataFrame
from colorama import init, Fore, Style
from time import time
from os import remove

# tuples of (benchmarked subject, compile command, run command, files to clean up)
TARGETS = [
	("Java", ["javac", "MatrixMultiplication.java"], ["java", "MatrixMultiplication"], ["MatrixMultiplication.class"]),
	("C", ["gcc", "matrix.c", "-o", "matrix"], ["./matrix"], ["matrix"]),
	("C[-O2]", ["gcc", "-O2", "matrix.c", "-o", "matrix_O2"], ["./matrix_O2"], ["matrix_O2"]),
	("C[-O3]", ["gcc", "-O3", "matrix.c", "-o", "matrix_O3"], ["./matrix_O3"], ["matrix_O3"]),
	("C++", ["g++", "matrix.cpp", "-o", "matrix_cpp"], ["./matrix_cpp"], ["matrix_cpp"]),
	("C++[-O2]", ["g++", "-O2", "matrix.cpp", "-o", "matrix_cpp_O2"], ["./matrix_cpp_O2"], ["matrix_cpp_O2"]),
	("C++[-O3]", ["g++", "-O3", "matrix.cpp", "-o", "matrix_cpp_O3"], ["./matrix_cpp_O3"], ["matrix_cpp_O3"]),
	("Python", None, ["python3", "matrix.py"], None),
	("Go", None, ["go", "run", "matrix.go"], None),
	("Rust", ["rustc", "matrix.rs", "-o", "matrix_rust"], ["./matrix_rust"], ["matrix_rust"])
]

# number of iterations
ITERATIONS = 5

init(autoreset=True)

class NonZeroExitCodeException(Exception):
	def __init__(self, message):
		super().__init__(message)

def compile(target, iter_num: int) -> float:
	print(f"{Fore.RED}Iteration {Style.BRIGHT}{iter_num}{Style.NORMAL}/{ITERATIONS}{Fore.RESET} --- {Fore.GREEN}Compiling subject {target[0]}.")
	start = time()

	process = Popen(target[1])
	process.wait()

	if process.returncode != 0:
		raise NonZeroExitCodeException(" ".join(target[1]))

	end = time()
	elapsed = end - start
	print(f"{Fore.RED}Iteration {Style.BRIGHT}{iter_num}{Style.NORMAL}/{ITERATIONS}{Fore.RESET} --- {Fore.YELLOW}Compilation of subject {target[0]} finished in {Style.BRIGHT}{elapsed}{Style.NORMAL} seconds.")
	return elapsed

def run(target, iter_num: int) -> float:
	print(f"{Fore.RED}Iteration {Style.BRIGHT}{iter_num}{Style.NORMAL}/{ITERATIONS}{Fore.RESET} --- {Fore.GREEN}Running subject {target[0]}.")

	process = Popen(target[2], stdout=PIPE, stderr=PIPE)
	process.wait()

	if process.returncode != 0:
		raise NonZeroExitCodeException(" ".join(target[1]))

	elapsed = float("\n".join([i.decode("utf-8") for i in process.stdout.readlines()]).strip())
	print(f"{Fore.RED}Iteration {Style.BRIGHT}{iter_num}{Style.NORMAL}/{ITERATIONS}{Fore.RESET} --- {Fore.YELLOW}Running of subject {target[0]} finished in {Style.BRIGHT}{elapsed}{Style.NORMAL} seconds.")
	return elapsed

if __name__ == "__main__":
	compilation_times = {}
	running_times = {}

	for target in TARGETS:
		for iteration in range(ITERATIONS):
			compilation_time = 0
			if target[1] is not None:
				compilation_time = compile(target, iteration + 1)
			running_time = run(target, iteration + 1)

			compilation_times.setdefault(target[0], []).append(compilation_time)
			running_times.setdefault(target[0], []).append(running_time)

			if target[3] is not None:
				for file in target[3]:
					remove(file)

	c_df = DataFrame(compilation_times)
	print("\n\n\n---     Compilation times     ---\n", c_df)
	print("\n--- Compilation average times ---\n\n", c_df.mean())
	r_df = DataFrame(running_times)
	print("\n\n\n---       Running times       ---\n", r_df)
	print("\n---   Running average times   ---\n\n", r_df.mean())