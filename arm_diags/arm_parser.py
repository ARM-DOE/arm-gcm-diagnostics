import ast
import cdp.cdp_parser
#from arm_diags import arm_parameter     # from . import arm_parameter
import arm_parameter

class ARMParser(cdp.cdp_parser.CDPParser):
    def __init__(self, *args, **kwargs):
        super(ARMParser, self).__init__(arm_parameter.ARMParameter, *args, **kwargs)

    #def load_default_args(self, *args):
    def load_default_args(self, files=[]):
        # this has '-p' and '--parameter' reserved
        super(ARMParser, self).load_default_args(files)

        self.add_argument(
            '-p', '--parameters',
            type=str,
            dest='parameters',
            help='Path to the user-defined parameter file',
            required=False)

        self.add_argument(
            '--base_path',
            type=str,
            dest='base_path',
            help='Path to arm_diags',
            required=False)

        self.add_argument(
            '--test_data_path',
            type=str,
            dest='test_data_path',
            help='Path to test data',
            required=False)

        self.add_argument(
            '--obs_path',
            type=str,
            dest='obs_path',
            help='Path to ARM obs data',
            required=False)

        self.add_argument(
            '--cmip_path',
            type=str,
            dest='cmip_path',
            help='Path to cmip data',
            required=False)

        self.add_argument(
            '--output_path',
            type=str,
            dest='output_path',
            help='Path to output data',
            required=False)

        self.add_argument(
            '-m', '--models',
            type=str,
            nargs='+',
            dest='models',
            help='Models to use',
            required=False)

        self.add_argument(
            '-r', '--reference_data_set',
            type=str,
            dest='reference_data_set',
            help='List of observations or models that are used as a ' +
                 'reference against the test_data_set',
            required=False)

        self.add_argument(
            '--reference_data_path',
            dest='reference_data_path',
            help='Path for the reference climitologies',
            required=False)

        self.add_argument(
            '-t', '--test_data_set',
            type=str,
            dest='test_data_set',
            help='List of observations or models to test ' +
                 'against the reference_data_set',
            required=False)

        self.add_argument(
            '--test_data_path',
            dest='test_data_path',
            help='Path for the test climitologies',
            required=False)

        self.add_argument(
            '-v', '--variables',
            type=str,
            dest='variables',
            help='Variables to use',
            required=False)

        self.add_argument(
            '--sites',
            type=str,
            dest='sites',
            help='sites to be evaluated',
            required=False)

        self.add_argument(
            '--plev',
            type=float,
            dest='plev',
            help='Selected pressure level',
            required=False)

        self.add_argument(
            '-s', '--season',
            type=str,
            nargs='+',
            dest='season',
            help='Season to use',
            required=False)

        self.add_argument(
            '--case_id',
            dest='case_id',
            help='Defines a subdirectory to the metrics output, so multiple' +
                 'cases can be compared',
            required=False)

        self.add_argument(
            '-o', '--output_file',
            dest='output_file',
            help='Name of the output file',
            required=False)

        self.add_argument(
            '--reference_name',
            dest='reference_name',
            help='Name of the reference variable',
            required=False)

        self.add_argument(
            '--test_name',
            dest='test_name',
            help='Name of the test variable',
            required=False)

        self.add_argument(
            '--diff_name',
            dest='diff_name',
            help='Name of the difference variable',
            required=False)

        self.add_argument(
            '--main_title',
            dest='main_title',
            help='The big title that appears on the top of the graph',
            required=False)

        self.add_argument(
            '--reference_title',
            dest='reference_title',
            help='Title for the middle graph.',
            required=False)

        self.add_argument(
            '--test_title',
            dest='test_title',
            help='Title for the top graph',
            required=False)

        self.add_argument(
            '--diff_title',
            dest='diff_title',
            help='Title for the bottom graph',
            required=False)

        self.add_argument(
            '--reference_colormap',
            dest='reference_colormap',
            help='Colormap for the middle graph.',
            required=False)

        self.add_argument(
            '--test_colormap',
            dest='test_colormap',
            help='Colormap for the top graph',
            required=False)

        self.add_argument(
            '--diff_colormap',
            dest='diff_colormap',
            help='Colormap for the bottom graph',
            required=False)


        self.add_argument(
            '--arm_filename',
            dest='arm_filename',
            help='Using files with ARM naming convention.',
            action='store_const',
            const=True,
            required=False)
