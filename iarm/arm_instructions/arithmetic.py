import iarm.exceptions
from ._meta import _Meta


class Arithmetic(_Meta):
    def ADCS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rb, Rc))

        def ADCS_func():
            self.register[Ra] = self.register[Rb] + self.register[Rc]
            self.register[Ra] += 1 if (self.register['APSR'] & (1 << 29)) else 0
            self.set_NZCV_flags(self.register[Rb], self.register[Ra])

        return ADCS_func

    def ADD(self, params):
        Rx, Ry, Rz = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rz):
            # ADD Rx, Ry, Rz
            self.check_arguments(any_registers=(Rx, Ry, Rz))
            if Rx != Ry:
                raise iarm.exceptions.RuleError("Second parameter {} does not equal first parameter {}". format(Ry, Rx))

            def ADD_func():
                self.register[Rx] = self.register[Ry] + self.register[Rz]
        else:
            if Rx == 'SP':
                # ADD SP, SP, #imm9_4
                self.check_arguments(imm9_4=(Rz,))
                if Rx != Ry:
                    raise iarm.exceptions.RuleError("Second parameter {} is not SP".format(Ry))
            else:
                # ADD Rx, [SP, PC], #imm10_4
                self.check_arguments(any_registers=(Rx,), imm10_4=(Rz,))
                if Ry not in ('SP', 'PC'):
                    raise iarm.exceptions.RuleError("Second parameter {} is not SP or PC".format(Ry))

            def ADD_func():
                self.register[Rx] = self.register[Ry] + int(Rz[1:])

        return ADD_func

    def ADDS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(self.THREE_PARAMETER_COMMA_SEPARATED, params)

        if self.is_register(Rc):
            # ADDS Ra, Rb, Rc
            self.check_arguments(low_registers=(Ra, Rb, Rc))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + self.register[Rc]
                self.set_NZCV_flags(self.register[Rb], self.register[Ra])
        elif Ra == Rb:
            # ADDS Ra, Ra, #imm8
            self.check_arguments(low_registers=(Ra,), imm8=(Rc,))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + int(Rc[1:])
                self.set_NZCV_flags(self.register[Rb], self.register[Ra])
        else:
            # ADDS Ra, Rb, #imm3
            self.check_arguments(low_registers=(Ra, Rb), imm3=(Rc,))

            def ADDS_func():
                self.register[Ra] = self.register[Rb] + int(Rc[1:])
                self.set_NZCV_flags(self.register[Rb], self.register[Ra])

        return ADDS_func

    def CMN(self, params):
        Ra, Rb = self.get_two_parameters(self.TWO_PARAMETER_COMMA_SEPARATED, params)

        self.check_arguments(low_registers=(Ra, Rb))

        def CMN_func():
            # TODO add the two but dont store result
            self.set_NZCV_flags(self.register[Ra], self.register[Ra] + self.register[Rb])

        return CMN_func

    def CMP(self, params):
        Ra, Rb = self.get_two_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def MULS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def NOP(self, params):
        def NOP_func():
            return
        return NOP_func

    def RSBS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def SBCS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def SUB(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func

    def SUBS(self, params):
        Ra, Rb, Rc = self.get_three_parameters(r'\s*([^\s,]*),\s*([^\s,]*)(,\s*[^\s,]*)*\s*', params)

        raise iarm.exceptions.NotImplementedError

        def UXTH_func():
            raise NotImplementedError

        return UXTH_func