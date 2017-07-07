#!/usr/bin/env python3.4

"""Filter common types of coordinate lines in the PDB according to specified options."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_filter_lines( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None
        self.noatom = args.noatom if args is not None else None
        self.onlystandard = args.onlystandard if args is not None else None
        self.hetatm = args.hetatm if args is not None else None
        self.ter = args.ter if args is not None else None
        self.end = args.end if args is not None else None
        self.model = args.model if args is not None else None
        self.water = args.water if args is not None else None
        return

    def run( self ):

        """The main function."""

        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.noatom is None: self.noatom = False
        if self.onlystandard is None: self.onlystandard = False
        if self.hetatm is None: self.hetatm = False
        if self.ter is None: self.ter = False
        if self.end is None: self.end = False
        if self.model is None: self.model = False
        if self.water is None: self.water = False

        # handle the input PDB file and only show lines that pass filter
        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:
                if self.show_line( line ):
                    print( line.strip() )
                else:
                    pass # line does adhere to option flag filters

        return 

    def show_line( self, in_line ):

        """Find and return matches according to input option flags."""

        # common lists to filter lines (e.g. standard 3-letter amino acid and water codes)
        aa_list = [ 'ALA', 'CYS', 'ASP', 'GLU', 'PHE', 
                    'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 
                    'MET', 'PRO', 'ARG', 'GLN', 'ASN',
                    'SER', 'THR', 'TRP', 'TYR', 'VAL' ]
        water_list =  [ 'HOH', 'WAT', 'H2O', 'TP3', 'TP5' ]

        # check line against option flags
        if not self.noatom and in_line[0:4] == 'ATOM':
            if self.onlystandard and not in_line[17:20] in aa_list:
                return False
            else:
                return in_line
        elif self.hetatm and in_line[0:6] == 'HETATM':
            return in_line
        elif self.ter and in_line[0:3] == 'TER':
            return in_line
        elif self.end and in_line[0:3] == 'END':
            return in_line
        elif self.model and ( in_line[0:5] == 'MODEL' or in_line[0:6] == 'ENDMDL' ):
            return in_line
        elif self.water and in_line[17:20] in water_list:
            return in_line
        else:
            return False # do not show non-matching lines
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-na', '--noatom', dest='noatom', required=False, help='hide ATOM lines', default=False, action='store_true' )
    parser.add_argument( '-aa', '--onlystandard', dest='onlystandard', required=False, help='show only standard twenty amino acid', default=False, action='store_true' )
    parser.add_argument( '-he', '--hetatm', dest='hetatm', required=False, help='show HETATM lines', default=False, action='store_true' )
    parser.add_argument( '-t', '--ter', dest='ter', required=False, help='show TER lines', default=False, action='store_true' )
    parser.add_argument( '-e', '--end', dest='end', required=False, help='show END lines', default=False, action='store_true' )
    parser.add_argument( '-m', '--model', dest='model', required=False, help='show MODEL lines', default=False, action='store_true' )
    parser.add_argument( '-w', '--water', dest='water', required=False, help='show water lines', default=False, action='store_true' )

    # command line execution
    main = pdb_filter_lines( args=parser.parse_args() )
    main.run()
