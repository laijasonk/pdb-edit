#!/usr/bin/env python3.4

"""Remove non-backbone atoms from PDB file (hydrogens, C-beta, non-Calpha atoms optional)."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_backbone_only( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None
        self.show_hydrogen = args.showHydrogen if args is not None else None
        self.show_cbeta = args.showCbeta if args is not None else None
        self.show_only_calpha = args.showOnlyCalpha if args is not None else None
        self.show_hetatm = args.showHetatm if args is not None else None
        return

    def run( self ):

        """The main function."""

        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.show_hydrogen is None: self.show_hydrogen = False
        if self.show_cbeta is None: self.show_cbeta = False
        if self.show_only_calpha is None: self.show_only_calpha = False
        if self.show_hetatm is None: self.keep_hetatm = False

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

        # common lists to filter lines (e.g. backbone heavy atoms, backbone hydrogens)
        bb_heavy = [ 'N  ', 'CA ', 'C  ', 'O  ' ]
        bb_hydrogen = [ 'H  ', 'HA ' ]

        # check line against option flags
        if self.show_hetatm and in_line[0:6] == 'HETATM':
            return in_line
        if in_line[0:4] == 'ATOM':
            if self.show_only_calpha and not in_line[13:16] == 'CA ':
                return False
            elif self.show_hydrogen and in_line[13:16] in bb_hydrogen:
                return in_line
            elif self.show_cbeta and in_line[13:16] == 'CB ':
                return in_line
            elif in_line[13:16] in bb_heavy:
                return in_line
            else:
                pass # not a backbone ATOM
        else:
            pass # not a ATOM coordinate line
        
        return False
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-hb', '--showHydrogen', dest='showHydrogen', required=False, help='show backbone hydrogens', default=False, action='store_true' )
    parser.add_argument( '-b', '--showCbeta', dest='showCbeta', required=False, help='show C-beta atoms (except for Glycine)', default=False, action='store_true' )
    parser.add_argument( '-a', '--showOnlyCalpha', dest='showOnlyCalpha', required=False, help='show only C-alpha atoms', default=False, action='store_true' )
    parser.add_argument( '-he', '--showHetatm', dest='showHetatm', required=False, help='include hetatm in output (no filter)', default=False, action='store_true' )

    # command line execution
    main = pdb_backbone_only( args=parser.parse_args() )
    main.run()
