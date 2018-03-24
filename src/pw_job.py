import subprocess
import shutil
import os

import pw_objectify_output

class PWJobRunner:
    def __init__(self, base_path, program_path='pw.x'):
        self.program_path = program_path
        self.base_path = base_path
    def create_dir(self, test_name):
        test_dir = os.path.join(self.base_path, test_name)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        os.mkdir(test_dir)
    def save_input(self, test_name, input_string, input_file_name='input'):
        input_file_path = os.path.join(self.base_path, test_name, input_file_name)
        with open(input_file_path, 'w', encoding='utf8') as f:
            f.write(input_string)
    def run_test(self, test_name, input_file_name='input', output_file_name='output', error_file_name='error'):
        #input_file_path = os.path.join(self.base_path, test_name, input_file_name)
        output_dir = os.path.join(self.base_path, test_name)
        output_file_path = os.path.join(self.base_path, test_name, output_file_name)
        error_file_path = os.path.join(self.base_path, test_name, error_file_name)
        with open(output_file_path, 'wb') as out:
            with open(error_file_path, 'wb') as err:
                subprocess.call([self.program_path, '-in', input_file_name],
                    cwd=output_dir,
                    stdout=out,
                    stderr=err)
    def run(self, test_name, input_string, input_file_name='input', output_file_name='output', error_file_name='error', skip_exists=False):
        test_dir = os.path.join(self.base_path, test_name)
        output_xml_path = os.path.join(self.base_path, test_name, 'pwscf.xml')
        if not skip_exists or not os.path.exists(test_dir):
            self.create_dir(test_name)
            self.save_input(test_name, input_string)
            self.run_test(test_name, input_file_name, output_file_name, error_file_name)
        parser = pw_objectify_output.PWObjectifyOutputParser()
        return parser.parse(output_xml_path)
