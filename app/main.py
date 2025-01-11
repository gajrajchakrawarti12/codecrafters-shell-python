import sys

def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        user_input = input()
        if user_input == "exit 0":
            break

        elif user_input.split(" ")[0] == "echo":
            print(user_input.split(' ', 1)[1])

        elif user_input.split(" ")[0] == "type":
            if user_input.split(" ")[1] in ["echo", "exit", "type"]:
                print(user_input.split(" ")[1] + " is a shell builtin")
            else:
                print(user_input.split(" ")[1] + " not found")
        else:
            print(f"{user_input}: command not found")
            
    



if __name__ == "__main__":
    main()
