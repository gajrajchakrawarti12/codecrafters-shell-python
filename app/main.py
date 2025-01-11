import sys
import os

def main():
    builtin_cmds = ["echo", "exit", "type"]
    PATH = os.environ.get("PATH")
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        user_input = input()
        if user_input == "exit 0":
            break

        elif user_input.split(" ")[0] == "echo":
            sys.stdout.write(user_input.split(' ', 1)[1] + "\n")

        elif user_input.split(" ")[0] == "type":
            cmd = user_input.split(" ")[1]
            cmd_path = None
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    cmd_path = f"{path}/{cmd}"
            
            if cmd in builtin_cmds:
                sys.stdout.write(cmd + " is a shell builtin\n")

            elif cmd_path:
                sys.stdout.write(f"{cmd} is {cmd_path}\n")
                
            else:
                sys.stdout.write(cmd + " not found\n")

        else:
            sys.stdout.write(f"{user_input}: command not found\n")
            
    



if __name__ == "__main__":
    main()
