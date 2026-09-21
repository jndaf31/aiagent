from functions.get_file_content import get_file_content

tests = [
    ("calculator", "lorem.txt"),   
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py")
]

for test in tests:

    result = get_file_content(*test)

    if test[1] == "lorem.txt":
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")
    else:
        print(result)