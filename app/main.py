import sys
commands = set()

def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Wait for user input
    user_input = input()
    if user_input not in commands:
        if user_input == "exit 0":
            return
        print(f"{user_input}: command not found")
        main()
    



if __name__ == "__main__":
    main()
