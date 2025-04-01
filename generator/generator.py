import os
import subprocess
import re
root_path=os.path.dirname(os.path.abspath(__file__))+'/../'

class Generator:
    def __init__(self, template: str, platform: str, architecture: str, target_location: str, output_format: str,
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
        self.target_location = target_location
        self.output_format = output_format
        self.key = key
        self.payload = payload
        self.values = values
        self.source = None
        self.template_content = None

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

        source_file = os.path.join(self.target_location, f'source.{template_type}')

        with open(source_file, 'w') as file:
            file.write(self.clean_output())

        compiler = compiler_switch[template_type]
        compile_command = [compiler, source_file]

        if self.platform == 'win':
            output_file = os.path.join(self.target_location, 'output')
            if self.output_format == 'exe':
                output_file += '.exe'
            else:
                output_file += '.dll'
                compile_command.append("-target:library")
        else:
            output_file = os.path.join(self.target_location, 'output')
            if self.output_format == 'elf-so':
                output_file += '.so'
            elif self.output_format == 'elf':
                output_file += '.elf'
        
        if template_type == 'cs':
            compile_command.append(output_file_argument[template_type]+output_file)
        else:
            compile_command.append(output_file_argument[template_type])
            compile_command.append(output_file)

        try:
            subprocess.run(compile_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")

    def generate_script(self) -> None:
        """
        Generate the script file with the source code
        """
        script_file = os.path.join(self.target_location, f'output.{self.output_format}', )
        with open(script_file, 'w') as file:
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

            if not os.path.exists(self.target_location):
                os.makedirs(self.target_location)

            if self.output_format in ['sh', 'bat', 'ps1', 'py', 'js', 'vba', 'hta']:
                self.generate_script()
            else:
                self.compile_source()
        except Exception as e:
            print(f"Error: {e}")

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





