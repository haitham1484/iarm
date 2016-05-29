import unittest
import iarm.iarm
import iarm.exceptions
import random


class TestArm(unittest.TestCase):
    """The base class for all arm tests"""
    def setUp(self):
        self.interp = iarm.iarm.Arm(32, 16, 1024, 8, False)


class TestArmParsing(TestArm):
    """
    Test all parsing exceptions
    """
    def test_bad_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError):
            self.interp.evaluate(' MOVS R1, 123')

    def test_no_parameters(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS')
        self.assertIn('None', str(cm.exception))

    def test_missing_first_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS ,')
        self.assertIn('first', str(cm.exception))

    def test_one_parameters(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1,')
        self.assertIn('second', str(cm.exception))

    def test_extra_argument(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1, #123, 456')
        self.assertIn('Extra', str(cm.exception))

    def test_missing_comma(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS R1 #123')
        self.assertIn('comma', str(cm.exception))

    def test_unknown_parameter(self):
        with self.assertRaises(iarm.exceptions.ParsingError) as cm:
            self.interp.evaluate(' MOVS abc, 123')
        self.assertIn('Unknown', str(cm.exception))


class TestArmValidation(TestArm):
    """
    Test validation errors
    """
    def test_bad_instruction(self):
        with self.assertRaises(iarm.exceptions.ValidationError):
            self.interp.evaluate(' BADINST')


class TestArmRules(TestArm):
    """
    Test all validation rules
    """
    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_none(self):
        with self.assertRaises(iarm.exceptions.RuleError):
            self.interp.evaluate(' MOVS')

    def test_parameter_not_register(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            self.interp.evaluate(' MOVS #1, #3')
        self.assertIn('not a register', str(cm.exception))

    def test_parameter_register_not_defined(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            self.interp.evaluate(' MOVS R{}, #3'.format(self.interp._max_registers+1))
        self.assertIn('greater', str(cm.exception))

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_not_an_immediate(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_not_an_immediate_unsigned(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_immediate_out_of_range(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_immediate_not_multiple_of(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass

    @unittest.skip('Currently there are no instructions to test that raise this type of exception')
    def test_parameter_low_register(self):
        with self.assertRaises(iarm.exceptions.RuleError) as cm:
            pass


class TestArmArithmetic(TestArm):
    """
    Test all arithmetic instructions
    """


class TestArmLinkedRegisters(TestArm):
    """
    Make sure that PC, LR, and SP are linked to R15, R14, and R13 respectively
    """
    def test_PC_register_link(self):
        REG1 = 'PC'
        REG2 = 'R15'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2**self.interp._bit_width-1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])

    def test_LR_register_link(self):
        REG1 = 'LR'
        REG2 = 'R14'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2 ** self.interp._bit_width - 1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])

    def test_SP_register_link(self):
        REG1 = 'SP'
        REG2 = 'R13'
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG1] = 0
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])
        self.interp.register[REG2] = 1
        self.assertEqual(self.interp.register[REG1], 1)
        self.interp.register[REG1] = random.randint(0, 2 ** self.interp._bit_width - 1)
        self.assertEqual(self.interp.register[REG1], self.interp.register[REG2])

if __name__ == '__main_':
    unittest.main()
