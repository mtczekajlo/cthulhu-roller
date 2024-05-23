from cthulhu_roller import main as cthulhu_roller
import argparse
import os
import subprocess
from tempfile import NamedTemporaryFile

def run():
    try:
        cthulhu_roller()
    except SystemExit:
        pass

def install():
    parser = argparse.ArgumentParser(
    prog="",
    description="",
  )
    parser.add_argument("--user", default=os.environ["USER"])
    parser.add_argument("--token", required=True)
    parser.add_argument("--service-path", required=True)
    args = parser.parse_args()
    service_file_content= f"""
[Unit]
Description=Cthulhu Roller bot service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User={args.user}
Environment=DISCORD_TOKEN={args.token}
ExecStart={args.service_path}

[Install]
WantedBy=multi-user.target
"""
    with NamedTemporaryFile() as fp:
        fp.write(service_file_content.encode())
        fp.flush()
        subprocess.call(['sudo', 'cp', f'{fp.name}', '/etc/systemd/system/cthulhu-roller.service'])
