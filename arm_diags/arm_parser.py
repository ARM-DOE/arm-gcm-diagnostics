import ast
import cdp.cdp_parser
from arm_diags import arm_parameter     # from . import arm_parameter


class ARMParser(cdp.cdp_parser.CDPParser):
    def __init__(self, *args, **kwargs):
        super(ARMParser, self).__init__(arm_parameter.ARMParameter, *args, **kwargs)

   
