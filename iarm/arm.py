#!/usr/bin/env python3

import iarm.exceptions
import iarm.arm_instructions as instructions


class Arm(instructions.DataMovement, instructions.Arithmetic,
          instructions.Logic, instructions.Shift, instructions.Memory,
          instructions.ConditionalBranch, instructions.UnconditionalBranch,
          instructions.Misc, instructions.Directives):

    def __init__(self, *args, **kwargs):
        super().__init__(32, 16, 8, *args, **kwargs)
        self.register.link('PC', 'R15')
        self.register.link('LR', 'R14')
        self.register.link('SP', 'R13')
        self.register['PC'] = 0

    def evaluate(self, code):
        parsed = self.parse_lines(code)

        # Find all labels (don't need to have them point to anything yet
        temp_labels = {line[0]: None for line in parsed if line[0]}
        self.labels.update(temp_labels)  # These will exist eventually in this code block

        # Validate the code and get back a function to execute that instruction
        program = []
        labels = {}
        for line in parsed:
            if not any(line):
                continue  # We have a blank line
            label, op, params = line

            # Set the label to the next instruction
            if label:
                # TODO how to integrate directives and instructions
                # TODO this doesnt take care of labels that are not jumps (like DCD)
                labels[label] = len(self.program) + len(program)

            # First, see if op is a directive
            # TODO raise an error if a directive is not where it should be
            if op in self.directives:
                try:
                    self.directives[op](label, params)  # Directives are run immediately
                    labels.update(self.labels)  # TODO find better way to keep these up to date so they are not over written by the `self.labels.update(labels)` step
                    continue
                except iarm.exceptions.IarmError:
                    [self.labels.pop(i, None) for i in temp_labels]  # Clean up the added labels

            # Next,
            # If the op lookup fails, it was a bad instruction
            if op:
                try:
                    func = self.ops[op]
                except KeyError:
                    [self.labels.pop(i, None) for i in temp_labels]  # Clean up the added labels
                    raise iarm.exceptions.ValidationError("Instruction {} does not exist".format(op))

                # Run the instruction, if it raised an error, roll back the labels
                try:
                    instruction = func(params)
                except Exception as e:
                    # TODO We may have a key error, or something other than an IarmError
                    [self.labels.pop(i, None) for i in temp_labels]  # Clean up the added labels
                    e.args = ("Error on '{}': ".format(label  + ' ' + op + ' ' + params),) + e.args
                    raise

                program.append(instruction)  # It validated, add it to the temp instruction list

        # Code block was successfully validated, update the main program
        self.program += program
        self.labels.update(labels)

        if not self._postpone_execution:
            self.run()

    def run(self, steps=float('inf')):
        """
        Run to the current end of the program or a number of steps
        :return:
        """
        while len(self.program) > self.register['PC']:
            steps -= 1
            if steps < 0:
                break
            self.program[self.register['PC']]()
            self.register['PC'] += 1

    def print_status_bits(self):
        print("N: {} Z: {} C: {} V: {}".format(
            int(self.is_N_set()),
            int(self.is_Z_set()),
            int(self.is_C_set()),
            int(self.is_V_set()),
        ))


if __name__ == '__main__':
    interp = Arm(1024, False, False)
