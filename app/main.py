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
    builtin_cmds = ["echo", "exit", "type"]
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

            if command == "exit":
                code = int(parts[1]) if len(parts) > 1 else 0
                sys.exit(code)

            elif command == "echo":
                if len(parts) > 1:
                    sys.stdout.write(parts[1])
                else:
                    sys.stdout.write()

            elif command == "type":
                if len(parts) < 2:
                    sys.stdout.write("type: missing argument")
                    continue
                
                cmd = parts[1]
                cmd_path = find_command_path(cmd, paths)
                
                if cmd in builtin_cmds:
                    sys.stdout.write(f"{cmd} is a shell builtin")
                elif cmd_path:
                    sys.stdout.write(f"{cmd} is {cmd_path}")
                else:
                    sys.stdout.write(f"{cmd}: command not found")
            
            else:
                cmd_path = find_command_path(command, paths)
                if cmd_path:
                    subprocess.run([cmd_path] + (parts[1:] if len(parts) > 1 else []))
                else:
                    sys.stdout.write(f"{command}: command not found")

        except Exception as e:
            sys.stdout.write(f"Error: {e}")

if __name__ == "__main__":
    main()
