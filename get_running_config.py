#import modules to run the commands below
import paramiko
import getpass

#this part defines parameters that will be used in the script
def get_running_config(target_device, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target_device, username=username, password=password, look_for_keys=False)
        command = "show running-config"
        stdin, stdout, stderr = ssh.exec_command(command)
        running_config = stdout.read().decode("utf-8")
        return running_config
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your username and password.")
    except paramiko.SSHException as e:
        print("Error:", str(e))
    finally:
        ssh.close()

#this part asks the user for target information and user credentials
def main():
    target_device = input("Enter the target device IP address: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    running_config = get_running_config(target_device, username, password)

#this section tells python where to write the config and what to name it
    if running_config:
        with open(target_device+".running_config.txt", "w") as file:
            file.write(running_config)
        print("Running configuration saved to"+ target_device +".running_config.txt")

if __name__ == "__main__":
    main()