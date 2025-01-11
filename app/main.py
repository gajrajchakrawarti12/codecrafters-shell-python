import sys
import os
import subprocess

def find_command_path(cmd, paths):
    for path in paths:
        cmd_path = os.path.join(path, cmd)
        if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
            return cmd_path
    return None

def main():
    builtin_cmds = ["echo", "exit", "type", "pwd"]
    path_env = os.environ.get("PATH", "")
    paths = path_env.split(os.pathsep)

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input().strip()
            if not user_input:
                continue

            parts = user_input.split(" ", 1)
            command = parts[0]

            match(command):
                case "exit":
                    code = int(parts[1]) if len(parts) > 1 else 0
                    sys.exit(code)

                case "pwd":
                    sys.stdout.write(os.getcwd() + "\n")

                case "cd":
                    if len(parts) > 1:
                        try:
                            os.chdir(os.path.expanduser(parts[1]))
                        except Exception as e:
                            sys.stdout.write(f"{": ".join(parts)}: No such file or directory\n")


                case "echo":
                    if len(parts) > 1:
                        string = parts[1].split("'")
                        sys.stdout.write(string + "\n")
                    else:
                        sys.stdout.write("\n")

                case "type":
                    if len(parts) < 2:
                        sys.stdout.write("type: missing argument\n")
                        continue
                    
                    cmd = parts[1]
                    cmd_path = find_command_path(cmd, paths)
                    
                    if cmd in builtin_cmds:
                        sys.stdout.write(f"{cmd} is a shell builtin\n")
                    elif cmd_path:
                        sys.stdout.write(f"{cmd} is {cmd_path}\n")
                    else:
                        sys.stdout.write(f"{cmd}: not found\n")
                
                case _:
                    cmd_path = find_command_path(command, paths)
                    if cmd_path:
                        subprocess.run(parts)
                    else:
                        sys.stdout.write(f"{command}: command not found\n")

        except Exception as e:
            sys.stdout.write(f"Error: {e}\n")

if __name__ == "__main__":
    main()
