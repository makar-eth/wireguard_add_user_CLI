import click
import os
import subprocess
from config import *

@click.command()
@click.argument('username', type=str)
def main(username):
    create_users_keys(username)
    publickey = subprocess.check_output(list(f"cat {username}_publickey".split()))
    privatekey = subprocess.check_output(list(f"cat {username}_privatekey".split()))
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
    conf.write(f"\n[Peer] \
        PublicKey = {publickey} \
        AllowedIPs = 10.0.0.{NUMBER}/32\n \
    ")
    conf.close()

def wireguard_reboot():
    os.system(f"systemctl restart wg-quick@{CONF_NAME}")
    os.system(f"systemctl status wg-quick@{CONF_NAME}")

def print_user_data(privatekey):
    click.echo(f"""\n[Interface]
        PrivateKey = {privatekey}
        Address = 10.0.0.{NUMBER}/32
        DNS = 8.8.8.8

        [Peer]
        PublicKey = {SERVER_PUBLICKEY}
        Endpoint = {SERVER_IP}:{PORT}
        AllowedIPs = 0.0.0.0/0
        PersistentKeepalive = 20\n
    """)

if __name__=='__main__':
    main()