import sys
import os
import subprocess
import re
root_path=os.path.dirname(os.path.abspath(__file__))+'/../'

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


class Generator:
    def __init__(self, template: str, platform: str, architecture: str, target_file: str, output_format: str,
                 key: str, payload: str, values: dict,
                 encrypt: str,
                 verbose: bool) -> None:
        """
        Initialize the Generator class
        """
        self.dev = False
        self.verbose = verbose
        self.encrypt = encrypt
        self.template = template
        self.platform = platform
        self.architecture = architecture
        self.target_file = target_file
        self.output_format = output_format
        self.key = key
        self.payload = payload
        self.values = values
        self.source = None
        self.template_content = None
        self.directory = ''

    def read_template(self) -> str:
        """
        Read the template file
        :return: str - Template content
        """
        template_path = os.path.join(root_path+'templates', self.template)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{self.template}' not found in './templates' directory.")
        with open(template_path, 'r') as file:
            return file.read()

    def substitute_values(self) -> str:
        """
        Substitute the values in the template
        :return: str - Source code with substituted values
        """
        self.source = self.template_content
        for key, value in self.values.items():
            if value is not None and f'[[{key}]]' in self.template_content:
                try:
                    float(value)
                    self.source = self.source.replace(f'"[[{key}]]"', value)
                except:
                    self.source = self.source.replace(f'[[{key}]]', value)


        return self.source

    def compile_source(self) -> None:
        """
        Compile the source code using the appropriate compiler
        """
        template_type = self.template.split('.')[1]  # Get the file extension
        if template_type not in ['c', 'cpp', 'cs', 'java', 'go']:
            raise ValueError(f"Unsupported template '{self.template}' for compilation")

        compiler_switch = {
            'c': 'gcc',
            'cpp': 'g++',
            'cs': 'mcs',
            'java': 'javac',
            'go': 'go build'
        }

        compiler_options = {
            'c': '-m32' if self.architecture == 'x86' else '-m64',
            'cpp': '-m32' if self.architecture == 'x86' else '-m64',
            'cs': '-platform:x86' if self.architecture == 'x86' else '-platform:x64',
            'java': '-d',
            'go': '--goarch=amd64' if self.architecture == 'x64' else '--goarch=386'
        }

        output_file_argument = {
            'c': '-o',
            'cpp': '-o',
            'cs': '-out:',
            'java': '',
            'go': '-o'
        }

        if self.target_file:

            compiler = compiler_switch[template_type]
            compile_command = [compiler]

            source_file = os.path.join(self.directory, f'source.{template_type}')

            with open(source_file, 'w') as file:
                file.write(self.clean_output())

            if template_type == 'cs':
                compile_command.append(output_file_argument[template_type]+self.target_file)
            else:
                compile_command.append(output_file_argument[template_type])
                compile_command.append(self.target_file)

            try:
                compile_command.append(source_file)
                subprocess.run(compile_command, check=True)
                print (f"{GREEN}[+] Compiled payload to {self.target_file}.{RESET}") 
            except subprocess.CalledProcessError as e:
                print(f"{RED}[-] Compilation failed: {e} {RESET}")
        else:
            print (f"{GREEN}[+] Compiled payload to {self.target_file}.{RESET}", file=sys.stderr) 
            print(self.clean_output())

    def generate_script(self) -> None:
        """
        Generate the script file with the source code
        """
        if self.target_file is None:
            print (f"{GREEN}[+] Your payload.{RESET}", file=sys.stderr) 
            print (self.clean_output())
        else:
            print (f"{GREEN}[+] Wrote payload to {self.target_file}.{RESET}", file=sys.stderr) 
            with open(self.target_file, 'w') as file:
                file.write(self.clean_output())

    def clean_output(self) -> str:
        """
        Clean the output by removing the first line, and removing any empty lines.
        if --dev is not set, it will remove any comments
        :return: str - Cleaned output
        """
        output = []
        for line in self.source.split('\n')[1:]:
            if self.output_format in ['ps1', 'py', 'sh', 'bat'] and line.startswith('#') and not self.dev:
                continue
            elif self.output_format in ['exe', 'elf', 'dll', 'elf-so'] and line.startswith('//') and not self.dev:
                continue
            elif line.strip() == '':
                continue
            output.append(line)

        return '\n'.join(output)

    def generate_payload(self) -> None:
        """
        Generate the payload
        """
        try:
            self.template_content = self.read_template()
            self.substitute_values()
            self.add_encryption()

            
            if self.target_file:
                self.directory = os.path.dirname(self.target_file)
            
            if self.target_file and self.directory == '':
                self.directory = os.getcwd()

            if self.target_file and not os.path.exists(self.directory) and not os.path.isdir(self.directory):
                print(f"{RED}[-] The output directory does not exist{RESET}")
                sys.exit()

            if self.output_format in ['sh', 'bat', 'ps1', 'py', 'js', 'vba', 'hta']:
                self.generate_script()
            else:
                self.compile_source()
        except Exception as e:
            print(f"{RED}[]Error: {e}{RESET}")

    @staticmethod
    def list_templates() -> None:
        """
        List the available templates
        :return:  list - List of available templates
        """
        templates_dir = root_path+'templates'

        if not os.path.exists(templates_dir):
            raise FileNotFoundError(f"Templates directory '{templates_dir}' not found.")
        templates = {}
        for template in os.listdir(templates_dir):
            if os.path.isfile(os.path.join(templates_dir, template)) and not template.startswith('.') and not template.endswith('.md') and template != 'LICENSE':
                templates[template] = open(os.path.join(templates_dir, template)).readline().strip()[3:]
        print("Available templates:")
        for template, description in templates.items():
            print(f"{template} \t- {description}")

    def add_encryption(self):
        encrypt_data = ""
        if self.encrypt != 'none':
            source_type = self.template.split('.')[-1]
            encrypt_path = os.path.join(root_path+'partial', f'{self.encrypt}.{source_type}')
            encrypt_data = ""
            if os.path.exists(encrypt_path):
                if not os.path.exists(encrypt_path):
                    raise FileNotFoundError(
                        f"Partial for encryptor '{self.encrypt}' not found in './partials' directory.")
                with open(encrypt_path, 'r') as file:
                    encrypt_data = file.read()
            self.source = self.source.replace(f'[[ENCRYPT]]', encrypt_data)
        else:
            keywords = ['[[KEY]]', '[[ENCRYPT]]']
            self.source = "\n".join(line for line in self.source.splitlines() if not any(keyword in line for keyword in keywords))





