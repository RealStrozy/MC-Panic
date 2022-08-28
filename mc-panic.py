import os
import configparser
import paramiko

# Def functions
parser = configparser.ConfigParser()


client = paramiko.SSHClient()


# Function to send commands over SSH
def ssh_command(execute):
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server_hostname, username=server_username, key_filename=server_key_filename, timeout=5)
        (stdin, stdout, stderr) = client.exec_command(execute)
        cmd_output = stdout.read()
        return cmd_output
    except RuntimeError:
        print("Unable to connect to SSH")


# Global vars
local_install_path = os.getcwd()


# Reads INI file
parser.read('%s/config.ini' % local_install_path)

# Pulls configs from files
try:
    # Server
    server_name = parser.get('server', 'server_name')
    mc_install_path = parser.get('server', 'mc_install_path')
    # SSH
    server_hostname = parser.get('SSH', 'server_hostname')
    server_username = parser.get('SSH', 'server_username')
    server_key_filename = parser.get('SSH', 'server_key_filename')

except configparser.NoSectionError:
    print("Reading config file failed.")

    name = input("Server name: ")
    mc_path = input("Minecraft server install path: ")
    host = input("Server hostname: ")
    user = input("Server username: ")
    key = input("SSH key for server: ")

    parser["server"] = {
        "server_name": name,
        "mc_install_path": mc_path,
    }

    parser["SSH"] = {
        "server_hostname": host,
        "server_username": user,
        "server_key_filename": key,
    }

    with open("config.ini", 'w') as output_file:
        parser.write(output_file)

    print("config.ini has been created. Please re-run this program to begin panicking.")
    exit(0)


# Pulling up keys for SSH
client.load_system_host_keys()

print("MC-Panic! Stop everything! Now!")
command_sp = input(
    "[1] Stop server \n[2] Kill all players \n[3] Set all payers to survival mode\n"
)

# Error checking for command
commands_list = ["1", "2", "3", "C"]
if command_sp not in commands_list:
    print("Command error")
    print(ssh_command('pwd'))
    exit(1)

# Run command and display output
if command_sp == "1":
    # noinspection PyUnboundLocalVariable
    ssh_command(f"nohup bash {mc_install_path}/stop.sh")

if command_sp == "2":
    # noinspection PyUnboundLocalVariable
    ssh_command(f"screen -S {server_name} -p 0 -X stuff 'gamemode s @a ^M kill @a ^M'")

if command_sp == "3":
    ssh_command(f"screen -S {server_name} -p 0 -X stuff 'gamemode s @a ^M'")

if command_sp == "C"
    exit(0)