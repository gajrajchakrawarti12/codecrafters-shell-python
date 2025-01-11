import sys
commands = set()

def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        user_input = input()
        if user_input == "exit 0":
            return
        elif user_input.split(" ")[0] == "echo":
            print(user_input.split(' ', 1)[1])
        else:
            print(f"{user_input}: command not found")
            
    



if __name__ == "__main__":
    main()
