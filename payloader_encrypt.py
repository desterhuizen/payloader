#!/usr/bin/env python3
import sys
import binascii
import argparse
import os

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def encrypt(encryption, data, key=42):
    enc=[]
    if encryption == 'xor':
        if isinstance(key, str):
            count = 0
            for b in data:
                enc_token = key[count % len(key)]
                enc.append(b ^ ord(enc_token))
                count += 1
        else:
            for b in data:
                enc.append(b ^ key)
    elif encryption in ['flop_flop','ff']:
        if isinstance(key, str):
            print (f"{RED}[-] Key must be a number for flip flop encryption.{RESET}", file=sys.stderr) 
            sys.exit(1)
        for b in data:
            key *= -1
            enc.append((b + int(key)) & 0xff)
    elif encryption in ['caesar']:
        if isinstance(key, str):
            print (f"{RED}[-] Key must be a number for caesar encryption.{RESET}", file=sys.stderr) 
            sys.exit(1)
        for b in data:
            enc.append((b + key) & 0xff)
    else:
        enc=data
    return bytes(enc)


def format_output(encrypted_data, language):
    """
    Format the encrypted data according to the specified language.
    """
    hex_output = binascii.hexlify(encrypted_data).decode('ascii')
    
    if language == "hex":
        return hex_output
    
    elif language == "python":
        return f"bytes.fromhex('{hex_output}')"
    
    elif language == "c":
        chunks = [hex_output[i:i+2] for i in range(0, len(hex_output), 2)]
        byte_string = ', '.join(f"0x{chunk}" for chunk in chunks)
        return f"unsigned char buf[] = {{\n  {byte_string}\n}};\n"
    
    elif language == "csharp" or language == "c#":
        chunks = [hex_output[i:i+2] for i in range(0, len(hex_output), 2)]
        byte_string = ', '.join(f"0x{chunk}" for chunk in chunks)
        return f"byte[] buf = new byte[] {{\n  {byte_string}\n}};\n"
    
    elif language == "java":
        chunks = [hex_output[i:i+2] for i in range(0, len(hex_output), 2)]
        byte_string = ', '.join(f"0x{chunk}" for chunk in chunks)
        return f"byte[] buf = new byte[] {{\n  {byte_string}\n}};\n"

    elif language == "powershell" or language == "ps1":
        chunks = [hex_output[i:i+2] for i in range(0, len(hex_output), 2)]
        byte_string = ','.join(f"0x{chunk}" for chunk in chunks)
        return f"[Byte[]] $buf = {byte_string}\n"
    
    elif language == "vba":
        # Convert bytes to decimal integers for VBA
        int_values = [b for b in encrypted_data]
        int_string = ','.join(str(val) for val in int_values)
        
        lines = []
        # Break into multiple lines for VBA's line length limitations
        current_line = "buf = Array("
        for i, val in enumerate(int_values):
            # Check if adding the next value would exceed line length
            if len(current_line + f"{val},") > 80 and i < len(int_values) - 1:
                lines.append(current_line.rstrip(",") + " _")
                current_line = "        "
            
            if i < len(int_values) - 1:
                current_line += f"{val},"
            else:
                current_line += f"{val}"
        
        lines.append(current_line + ")")
        return "\n".join(lines)

    elif language == "js" or language == "javascript":
        return f"const buf = new Uint8Array(Buffer.from('{hex_output}', 'hex'));"
    
    else:
        return f"Unsupported language: {language}. Using hex format instead:\n{hex_output}"

def parse_int_or_str(value):
    """Parse the value as int if possible, otherwise keep as string."""
    try:
        return int(value)
    except ValueError:
        return value

def main():
    parser = argparse.ArgumentParser(description='Encrypt binary data and output in specified format.')
    parser.add_argument('--key', type=parse_int_or_str, default=42, help='Encryption key.')
    parser.add_argument('--encryption', type=str, default='xor', help='Encryption algorithm.', choices=['xor', 'flip_flop', 'ff', 'caesar'])
    parser.add_argument('--lang', type=str, default='hex', 
                        choices=['hex', 'python', 'c', 'csharp', 'c#', 'java', 'vba', 'js', 'javascript','ps1', 'powershell'],
                        help='Output language format')
    parser.add_argument('--input', type=str, help='Input file path (if not specified, reads from stdin)')
    parser.add_argument('--output', type=str, help='Output file path (if not specified, writes to stdout)')
    
    args = parser.parse_args()
    
    # Read binary data from input file or stdin
    if args.input:
        with open(args.input, 'rb') as f:
            binary_data = f.read()
    else:
        # Check if stdin has data (piped input)
        if not os.isatty(sys.stdin.fileno()):
            binary_data = sys.stdin.buffer.read()
        else:
            print(f"{RED}[-] Error: No input provided. Either pipe data to the script or specify an input file.{RESET}")
            parser.print_help()
            sys.exit(1)
    
    # Encrypt the data with the specified key
    encrypted_data = encrypt(args.encryption, binary_data, args.key)
    
    # Format according to the specified language
    formatted_output = format_output(encrypted_data, args.lang.lower())
    
    print (f"{GREEN}[+] Encrypted using {args.encryption} and {args.key} as the key.{RESET}", file=sys.stderr)
    # Output to file or stdout
    if args.output:
        with open(args.output, 'w') as f:
            f.write(formatted_output)
        print(f"{GREEN}[+] Output written to {args.output}{RESET}")
    else:
        print(formatted_output)

if __name__ == "__main__":
    main()
