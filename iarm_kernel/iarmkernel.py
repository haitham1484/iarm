from ipykernel.kernelbase import Kernel
from iarm.arm import Arm


class ArmKernel(Kernel):
    implementation = 'IArm'
    implementation_version = '0.1'
    language = 'ARM'
    language_version = '0.1'
    language_info = {
        'name': 'ARM Coretex M0+ Assembly',
        'mimetype': 'text/x-asm',
        'file_extension': '.s'
    }
    banner = "Interpreted ARM"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interpreter = Arm(1024)  # 1K memory
        self.magics = {
            'run': self.magic_run,
            'register': self.magic_register,
            'reg': self.magic_register,
            'memory': self.magic_memory,
            'mem': self.magic_memory
                       }

    def magic_register(self, line):
        # TODO allow for ranges
        message = ""
        for reg in [i.strip() for i in line.replace(',', '').split()]:
            message += "{}: {}\n".format(reg, self.interpreter.register[reg])
        stream_content = {'name': 'stdout', 'text': message}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def magic_memory(self, line):
        # TODO allow for ranges
        message = ""
        for address in [i.strip() for i in line.replace(',', '').split()]:
            message += "{}: {}\n".format(address, self.interpreter.memory[address])
        stream_content = {'name': 'stdout', 'text': message}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def magic_run(self, line):
        i = float('inf')
        if line.strip():
            i = int(line)
        self.interpreter.run(i)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        # TODO allow magics at end of code block
        # TODO allow more than one magic per block
        if code.startswith('%'):
            loc = code.find(' ')
            params = ""
            if loc > 0:
                params = code[loc + 1:]
                op = code[1:loc]
            else:
                op = code[1:]
            self.magics[op](params)
        else:
            try:
                self.interpreter.evaluate(code)
            except Exception as e:
                stream_content = {'name': 'stderr', 'text': str(e)}
                self.send_response(self.iopub_socket, 'stream', stream_content)
                return {'status': 'error',
                        'execution_count': self.execution_count,
                        'ename': type(e).__name__,
                        'evalue': str(e),
                        'traceback': '???'}
        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}
                }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=ArmKernel)