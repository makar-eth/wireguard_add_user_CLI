import os
import click
from config import *

@click.command(help='This command create new user for your Wireguard VPN server. Then you call it with username, it\'s create public and private keys for user, adds them to .conf, reboot server with new user and return config sor user')
@click.argument('username', type=str)
def main(username):
    create_users_keys(username)
    os.system(f"cat {username}_privatekey > temp1.txt")
    with open('temp1.txt', 'r') as f:
         privatekey = f.read()
    os.system(f"cat {username}_publickey > temp2.txt")
    with open('temp2.txt', 'r') as f:
         publickey = f.read()
    os.system("rm temp1.txt")
    os.system("rm temp2.txt")
    if privatekey.endswith('\n'):
        privatekey = privatekey[:-1]
    if publickey.endswith('\n'):
        publickey = publickey[:-1]
    add_user_to_conf(publickey)
    wireguard_reboot()
    print_user_data(privatekey)

def create_users_keys(username):
    if os.path.exists(f"{username}_privatekey") or os.path.exists(f"{username}_publickey"):
        click.echo(f"{username} already exists.")
        exit(-1)
    else:
        os.system(f"wg genkey | tee /etc/wireguard/{username}_privatekey | wg pubkey | tee /etc/wireguard/{username}_publickey")

def add_user_to_conf(publickey):
    conf = open(CONF_PATH, 'a')
    print(publickey)
    conf.write(f"\n[Peer]\nPublicKey = {publickey}\nAllowedIPs = 10.0.0.{NUMBER}/32\n")
    conf.close()

def wireguard_reboot():
    os.system(f"systemctl restart wg-quick@{CONF_NAME}")
    os.system(f"systemctl status wg-quick@{CONF_NAME}")

def print_user_data(privatekey):
    click.echo(f"\n[Interface]\nPrivateKey = {privatekey}\nAddress = 10.0.0.{NUMBER}/32\nDNS = 8.8.8.8\n\n[Peer]\nPublicKey = {SERVER_PUBLICKEY}\nEndpoint = {SERVER_IP}:{PORT}\nAllowedIPs = 0.0.0.0/0\nPersistentKeepalive = 20\n")

if __name__=='__main__':
    main()