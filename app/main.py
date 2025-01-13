import sys
import os
import subprocess
import shlex

def find_command_path(cmd, paths):
    for path in paths:
        cmd_path = os.path.join(path, cmd)
        if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
            return cmd_path
    return None

def main():
    builtin_cmds = ["echo", "exit", "type", "pwd", "cd"]
    path_env = os.environ.get("PATH", "")
    paths = path_env.split(os.pathsep)

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
            if not user_input:
                continue

            parts = shlex.split(user_input, posix=True)
            command = parts[0]

            match(command):
                case "exit":
                    code = int(parts[1]) if len(parts) > 1 else 0
                    sys.exit(code)

                case "pwd":
                    sys.stdout.write(os.getcwd() + "\n")

                case "ls":
                    try:
                        if ">" in parts:
                            cmd_part = parts[:parts.index('>')]
                            output_file = parts[parts.index('>') + 1]
                            with open(output_file, 'w') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    print(f"Error: {result.stderr.strip()}")
                        elif "2>" in parts:
                            cmd_part = parts[:parts.index('2>')]
                            output_file = parts[parts.index('2>') + 1]
                            with open(output_file, 'w') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    f.write(str(result.stderr))
                        elif ">>" in parts:
                            cmd_part = parts[:parts.index('>>')]
                            output_file = parts[parts.index('>>') + 1]
                            with open(output_file, 'a') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    sys.stdout.write(str(result.stderr))
                        elif "2>>" in parts:
                            cmd_part = parts[:parts.index('2>>')]
                            output_file = parts[parts.index('2>>') + 1]
                            with open(output_file, 'a') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=f, text=True)
                    except subprocess.CalledProcessError as e:
                        sys.stdout.write(f"ls: {e.cmd}: {e.stderr}\n")

                case "cd":
                    try:
                        os.chdir(os.path.expanduser(parts[1]))
                    except Exception as e:
                        sys.stdout.write(f"{": ".join(parts)}: No such file or directory\n")


                case "echo":
                    try:   
                        if ">" in parts:
                            cmd_part = parts[:parts.index('>')]
                            output_file = parts[parts.index('>') + 1]
                            with open(output_file, 'w') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    print(f"Error: {result.stderr.strip()}")
                        elif "1>" in parts:
                            cmd_part = parts[:parts.index('1>')]
                            output_file = parts[parts.index('1>') + 1]
                            with open(output_file, 'w') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    print(f"Error: {result.stderr.strip()}")
                        elif "2>" in parts:
                            cmd_part = parts[:parts.index('2>')]
                            output_file = parts[parts.index('2>') + 1]
                            result = subprocess.run(cmd_part, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            with open(output_file, 'w') as f:  
                                sys.stdout.write(result.stdout)
                                if result.stderr:                
                                    f.write(str(result.stderr))
                        elif "1>>" in parts:
                            cmd_part = parts[:parts.index('1>>')]
                            output_file = parts[parts.index('1>>') + 1]
                            with open(output_file, 'a') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:                
                                    f.write(str(result.stderr))
                        elif "2>>" in parts:
                            cmd_part = parts[:parts.index('2>>')]
                            output_file = parts[parts.index('2>>') + 1]
                            with open(output_file, 'a') as f:
                                result = subprocess.run(cmd_part, stdout=subprocess.PIPE, stderr=f, text=True)
                                if result.stdout:
                                    sys.stdout.write(result.stdout)
                        else:
                            sys.stdout.write(" ".join(parts[1:]) + "\n")
                    except Exception as e:
                        sys.stdout.write(f"echo: {e}\n")

                case "cat":
                    try:
                        if "1>" in parts:
                            cmd_part = parts[:parts.index('1>')]
                            output_file = parts[parts.index('1>') + 1]
                            with open(output_file, 'w') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=subprocess.PIPE, text=True)
                                if result.stderr:
                                    sys.stdout.write(result.stderr)
                        elif "2>" in parts:
                            cmd_part = parts[:parts.index('2>')]
                            output_file = parts[parts.index('2>') + 1]
                            result = subprocess.run(cmd_part, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            with open(output_file, 'w') as f:  
                                sys.stdout.write(result.stdout)
                                if result.stderr:                
                                    f.write(str(result.stderr))
                        elif "2>>" in parts:
                            cmd_part = parts[:parts.index('2>>')]
                            output_file = parts[parts.index('2>>') + 1]
                            with open(output_file, 'a') as f:
                                result = subprocess.run(cmd_part, stdout=f, stderr=f, text=True)
                        else:
                            for i in parts[1:]:
                                if i not in ['', ' ']:
                                    with open(i, 'r') as file:
                                        sys.stdout.write(file.read())
                    except Exception as e:
                        sys.stdout.write(f"{": ".join(parts)}: No such file or directory\n")
                

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
