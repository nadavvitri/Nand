
class VMWriter:
    def __init__(self, file, file_name):
        if file is None:
            pass
        else:
            self.output_file = open(file + ".vm", "w")
            self.file_name = file_name

    def write_push(self, segment, index):
        vm_command = "push " + segment + " " + str(index) + "\n"
        self.output_file.write(vm_command)

    def write_pop(self, segment, index):
        vm_command = "pop " + segment + " " + str(index) + "\n"
        self.output_file.write(vm_command)

    def write_arithmetic(self, command):
        self.output_file.write(command + "\n")

    def write_label(self, label):
        vm_command = "label " + label + "\n"
        self.output_file.write(vm_command)

    def write_goto(self, label):
        vm_command = "goto " + label + "\n"
        self.output_file.write(vm_command)

    def write_if(self, label):
        vm_command = "if-goto " + label + "\n"
        self.output_file.write(vm_command)

    def write_call(self, name, n_args):
        if name == '*':
            name = "Math.multiply"
        if name == "/":
            name = "Math.divide"
        vm_command = "call " + name + " " + str(n_args) + "\n"
        self.output_file.write(vm_command)

    def write_function(self, name, n_locals):
        vm_command = "function " + self.file_name + "." + name + " " + str(n_locals) + "\n"
        self.output_file.write(vm_command)

    def write_return(self):
        self.output_file.write("return\n")

    def close(self):
        self.output_file.close()
