from functions.get_files_info import get_files_info

test_values = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

for test in test_values:
    if test[1] == ".":
        print(f"Result for current directory:")
    else:
        print(f"Result for {test[1]} directory:")
    print(get_files_info(*test))
