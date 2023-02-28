import sys
from subprocess import PIPE, Popen
import os
import argparse
import time


BASE = "anchor-wrapper"
# pyinstaller --onefile -n anchor-wrapper main.py
# anchor-wrapper init --type program test-app
parser = argparse.ArgumentParser(
    prog='anchor-wrapper',
    description='Initialize and run a container with Solana and Anchor pre-installed for faster and easier development on Solana using Anchor.'
)
parser.add_argument('action', choices=['init','start'], help='The command to run [init,start]')
parser.add_argument('app_name', metavar='app-name', help='Application name')
parser.add_argument('--type', '-t', nargs='?', choices=[
                    'program', 'client'], default='program', help='The type of project to create [program, client]')
parser.add_argument('--image', "-i", metavar='docker-image:tag',
                    nargs='+', default="ravthedoker/anchor-quick-launch", help='The Docker image to pull and run')
parser.add_argument('--command', "-c", metavar='override command', nargs='+', help='Override the container starting command')
parser.add_argument(
    '--port', "-p", help='The pair of ports to map to the container [host:container]')

args = parser.parse_args(sys.argv[1:])

# try and catch Ctrl+C and exit
try:
    if args.action == 'init':
        # create directory of app name and run the docker mount the directory
        print('Creating directory')
        os.system('mkdir ' + args.app_name)

        print('Pulling docker image')
        os.system('docker pull ' + args.image)

        command = ''
        # default command - program
        if args.command is not None:
            command = args.command
        else:
            command = f'anchor init {args.app_name}'

            print('Running docker container')
            if args.type == 'client':
                command = f'yarn create next-app --typescript --experimental-app --eslint --src-dir --import-alias "@/*" {args.app_name} && cd {args.app_name} && yarn add @project-serum/anchor @solana/web3.js @solana/wallet-adapter-react @solana/wallet-adapter-react-ui @solana/wallet-adapter-wallets @solana/wallet-adapter-base'

        exts = ''
        if args.port is not None:
            exts += f'''-p {args.port} '''

        tail ='tail -f /dev/null'
        
        host_target_dir = os.path.join(os.getcwd(),f'{args.app_name}\\').replace('\\','/')
        exts += f'''--mount src={host_target_dir},target=/app,type=bind '''

        run_command = f'''docker run -d --rm {exts}{args.image} bash -c "{command} && {tail}" '''

        os.system(run_command)
    elif args.action == 'start':
        print('Starting container')

        exts = ''
        # start the container
        if args.port is not None:
            exts += f'''-p {args.port} '''

        tail ='tail -f /dev/null'
        
        host_target_dir = os.path.join(os.getcwd()).replace('\\','/')
        exts += f'''--mount src={host_target_dir},target=/app/{args.app_name},type=bind '''

        run_command = f'''docker run -d --rm {exts}{args.image} bash -c "{tail}" '''

        os.system(run_command)
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)

finally:
    print("Exiting...")
    sys.exit(0)