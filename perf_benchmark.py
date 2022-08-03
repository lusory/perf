from subprocess import Popen, PIPE
from pandas import DataFrame
from colorama import init, Fore, Style
from time import time
from os import remove
from json import load, dump
from argparse import ArgumentParser
from os.path import isfile

# tuples of (benchmarked subject, compile command, run command, files to clean up)
TARGETS = [
    ("Java", ["javac", "MatrixMultiplication.java"], ["java", "MatrixMultiplication"], ["MatrixMultiplication.class"]), # 0
    ("C", ["gcc", "matrix.c", "-o", "matrix"], ["./matrix"], ["matrix"]), # 1
    ("C[-O2]", ["gcc", "-O2", "matrix.c", "-o", "matrix_O2"], ["./matrix_O2"], ["matrix_O2"]), # 2
    ("C[-O3]", ["gcc", "-O3", "matrix.c", "-o", "matrix_O3"], ["./matrix_O3"], ["matrix_O3"]), # 3
    ("C++", ["g++", "matrix.cpp", "-o", "matrix_cpp"], ["./matrix_cpp"], ["matrix_cpp"]), # 4
    ("C++[-O2]", ["g++", "-O2", "matrix.cpp", "-o", "matrix_cpp_O2"], ["./matrix_cpp_O2"], ["matrix_cpp_O2"]), # 5
    ("C++[-O3]", ["g++", "-O3", "matrix.cpp", "-o", "matrix_cpp_O3"], ["./matrix_cpp_O3"], ["matrix_cpp_O3"]), # 6
    ("Go", None, ["go", "run", "matrix.go"], None), # 7
    ("Rust", ["rustc", "-o", "matrix_rust", "matrix.rs"], ["./matrix_rust"], ["matrix_rust"]), # 8   
    ("Rust[-O2]", ["rustc", "-C", "opt-level=2", "-o", "matrix_rust_O2", "matrix.rs"], ["./matrix_rust_O2"], ["matrix_rust_O2"]), # 9
    ("Rust[-O3]", ["rustc", "-C", "opt-level=3", "-o", "matrix_rust_O3", "matrix.rs"], ["./matrix_rust_O3"], ["matrix_rust_O3"]), # 10
    # python is the slowest, so keep it at the end
    ("Python", None, ["python3", "matrix.py"], None) # 11
]

# number of iterations
ITERATIONS = 5

init(autoreset=True)


class NonZeroExitCodeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Benchmark:
    def __init__(self, targets, iterations: int, c_dumping_file: str, r_dumping_file: str):
        self.targets = targets
        self.iterations = iterations
        self.c_dumping_file = c_dumping_file
        self.r_dumping_file = r_dumping_file
        self.iter_num = 0
        if c_dumping_file is not None and isfile(c_dumping_file):
            with open(c_dumping_file, "r") as f:
                self.compilation_times = load(f)
        else:
            self.compilation_times = {}
        if r_dumping_file is not None and isfile(r_dumping_file):
            with open(r_dumping_file, "r") as f:
                self.running_times = load(f)
        else:
            self.running_times = {}

    def benchmark(self):
        for target in self.targets:
            for iteration in range(self.iterations):
                self.iter_num = iteration + 1

                compilation_time = 0
                if target[1] is not None:
                    compilation_time = self.compile(target)
                running_time = self.run(target)

                self.compilation_times.setdefault(target[0], []).append(compilation_time)
                self.running_times.setdefault(target[0], []).append(running_time)

                if target[3] is not None:
                    for file in target[3]:
                        remove(file)

                if self.c_dumping_file is not None:
                    with open(self.c_dumping_file, "w") as f:
                        dump(self.compilation_times, f)

                if self.r_dumping_file is not None:
                    with open(self.r_dumping_file, "w") as f:
                        dump(self.running_times, f)

    def compile(self, target) -> float:
        print(f"{Fore.RED}Iteration {Style.BRIGHT}{self.iter_num}{Style.NORMAL}/{self.iterations}{Fore.RESET} --- {Fore.GREEN}Compiling subject {target[0]}.")
        start = time()

        process = Popen(target[1])
        process.wait()

        if process.returncode != 0:
            raise NonZeroExitCodeException(" ".join(target[1]))

        end = time()
        elapsed = end - start
        print(f"{Fore.RED}Iteration {Style.BRIGHT}{self.iter_num}{Style.NORMAL}/{self.iterations}{Fore.RESET} --- {Fore.YELLOW}Compilation of subject {target[0]} finished in {Style.BRIGHT}{elapsed}{Style.NORMAL} seconds.")
        return elapsed

    def run(self, target) -> float:
        print(f"{Fore.RED}Iteration {Style.BRIGHT}{self.iter_num}{Style.NORMAL}/{self.iterations}{Fore.RESET} --- {Fore.GREEN}Running subject {target[0]}.")

        process = Popen(target[2], stdout=PIPE, stderr=PIPE)
        process.wait()

        if process.returncode != 0:
            raise NonZeroExitCodeException(" ".join(target[1]))

        elapsed = float("\n".join([i.decode("utf-8") for i in process.stdout.readlines()]).strip())
        print(f"{Fore.RED}Iteration {Style.BRIGHT}{self.iter_num}{Style.NORMAL}/{self.iterations}{Fore.RESET} --- {Fore.YELLOW}Running of subject {target[0]} finished in {Style.BRIGHT}{elapsed}{Style.NORMAL} seconds.")
        return elapsed

    def print_frames(self):
        c_df = DataFrame(self.compilation_times)
        print("\n\n\n---     Compilation times     ---\n", c_df)
        print("\n--- Compilation average times ---\n\n", c_df.mean())
        r_df = DataFrame(self.running_times)
        print("\n\n\n---       Running times       ---\n", r_df)
        print("\n---   Running average times   ---\n\n", r_df.mean())

if __name__ == "__main__":
    parser = ArgumentParser(description="Benchmarks programming languages.")
    parser.add_argument("--start", type=int, help="the index at which the target list starts", required=False, default=0)
    parser.add_argument("--end", type=int, help="the index at which the target list ends", required=False, default=len(TARGETS))

    args = parser.parse_args()

    benchmark = Benchmark(TARGETS[args.start:args.end], ITERATIONS, "compilation_times.json", "running_times.json")
    benchmark.benchmark()
    benchmark.print_frames()
