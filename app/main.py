import os
import sys
import shlex
import subprocess
from shutil import which

def handle_redirection(cmd_parts):
    """
    Handles I/O redirection for commands.
    Returns the modified cmd_parts, stdout file, and stderr file.
    """
    stdout = None
    stderr = None

    if '>' in cmd_parts or '>>' in cmd_parts or '1>' in cmd_parts or '1>>' in cmd_parts or '2>' in cmd_parts or '2>>' in cmd_parts:
        while '>' in cmd_parts:
            idx = cmd_parts.index('>')
            output_file = cmd_parts[idx + 1]
            stdout = open(output_file, 'w')
            cmd_parts = cmd_parts[:idx] + cmd_parts[idx + 2:]
        
        while '>>' in cmd_parts:
            idx = cmd_parts.index('>>')
            output_file = cmd_parts[idx + 1]
            stdout = open(output_file, 'a')
            cmd_parts = cmd_parts[:idx] + cmd_parts[idx + 2:]
        
        while '1>' in cmd_parts:
            idx = cmd_parts.index('1>')
            output_file = cmd_parts[idx + 1]
            stdout = open(output_file, 'w')
            cmd_parts = cmd_parts[:idx] + cmd_parts[idx + 2:]
        
        while '1>>' in cmd_parts:
            idx = cmd_parts.index('1>>')
            output_file = cmd_parts[idx + 1]
            with open(output_file, 'a') as f:
                result = subprocess.run(cmd_parts[:idx], stdout=f, stderr=subprocess.PIPE, text=True)
                if result.stderr:                
                    f.write(str(result.stderr))
        
        while '2>' in cmd_parts:
            idx = cmd_parts.index('2>')
            output_file = cmd_parts[idx + 1]
            stderr = open(output_file, 'w')
            cmd_parts = cmd_parts[:idx] + cmd_parts[idx + 2:]
        
        while '2>>' in cmd_parts:
            idx = cmd_parts.index('2>>')
            output_file = cmd_parts[idx + 1]
            stderr = open(output_file, 'a')
            cmd_parts = cmd_parts[:idx] + cmd_parts[idx + 2:]
    
    return cmd_parts, stdout, stderr

def execute_command(cmd_parts, stdout=None, stderr=None):
    """
    Executes the given command with optional stdout and stderr redirection.
    """
    try:
        subprocess.run(cmd_parts, stdout=stdout, stderr=stderr, text=True)
    except FileNotFoundError:
        sys.stderr.write(f"{cmd_parts[0]}: command not found\n")
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")

def builtin_cd(path):
    """
    Change the current working directory.
    """
    try:
        os.chdir(os.path.expanduser(path))
    except FileNotFoundError:
        sys.stderr.write(f"cd: {path}: No such file or directory\n")
    except Exception as e:
        sys.stderr.write(f"cd: {e}\n")

def builtin_type(cmd, builtin_cmds):
    """
    Prints information about a command (builtin or external).
    """
    cmd_path = which(cmd)
    if cmd in builtin_cmds:
        sys.stdout.write(f"{cmd} is a shell builtin\n")
    elif cmd_path:
        sys.stdout.write(f"{cmd} is {cmd_path}\n")
    else:
        sys.stderr.write(f"{cmd}: not found\n")

def main():
    """
    Main loop of the shell interpreter.
    """
    builtin_cmds = ["echo", "exit", "type", "pwd", "cd"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            user_input = input()
            if not user_input.strip():
                continue

            # Parse the command and handle redirection
            cmd_parts, stdout, stderr = handle_redirection(shlex.split(user_input, posix=True))
            if not cmd_parts:
                continue

            command = cmd_parts[0]

            # Handle built-in commands
            match command:
                case "exit":
                    code = int(cmd_parts[1]) if len(cmd_parts) > 1 else 0
                    sys.exit(code)

                case "pwd":
                    sys.stdout.write(os.getcwd() + "\n")

                case "cd":
                    if len(cmd_parts) < 2:
                        sys.stderr.write("cd: missing argument\n")
                    else:
                        builtin_cd(cmd_parts[1])

                case "type":
                    if len(cmd_parts) < 2:
                        sys.stderr.write("type: missing argument\n")
                    else:
                        builtin_type(cmd_parts[1], builtin_cmds)

                case "echo":
                    sys.stdout.write(" ".join(cmd_parts[1:]) + "\n")

                case _:
                    # Attempt to execute external commands
                    execute_command(cmd_parts, stdout=stdout, stderr=stderr)

            # Close any opened files
            if stdout:
                stdout.close()
            if stderr:
                stderr.close()

        except KeyboardInterrupt:
            sys.stdout.write("\n")
            continue
        except EOFError:
            sys.stdout.write("\nExiting shell.\n")
            break
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")

if __name__ == "__main__":
    main()
