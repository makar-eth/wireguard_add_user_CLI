import click
import os
import subprocess
from config import *

@click.command()
@click.argument('username', type=str)
def main(username):
    create_users_keys(username)

def create_users_keys(username):
    if os.path.exists(f"{username}_privatekey") or os.path.exists(f"{username}_publickey"):
        click.echo(f"{username} already exists.")
        exit(-1)
    else:
        os.system(f"wg genkey | tee /etc/wireguard/{username}_privatekey | wg pubkey | tee /etc/wireguard/{username}_publickey")


if __name__=='__main__':
    main()