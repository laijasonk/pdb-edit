#!/usr/bin/env python3.4

"""Filter common types of coordinate lines in the PDB."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_atom_hetatm_only( object ):
    def __init__( self, args=None ):
        """The class constructor."""
        self.pdb = args.pdb if args is not None else None
        self.hetatm = args.hetatm if args is not None else None
        self.ter = args.ter if args is not None else None
        self.end = args.end if args is not None else None
        self.model = args.model if args is not None else None
        return

    def run( self ):
        """The main function."""
        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.hetatm is None: self.hetatm = False
        if self.ter is None: self.ter = False
        if self.end is None: self.end = False
        if self.model is None: self.model = False

        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:
                if line[0:4] == 'ATOM':
                    print( line.strip() )
                elif self.hetatm and line[0:6] == 'HETATM':
                    print( line.strip() )
                elif self.ter and line[0:3] == 'TER':
                    print( line.strip() )
                elif self.end and line[0:3] == 'END':
                    print( line.strip() )
                elif self.model and ( line[0:5] == 'MODEL' or line[0:6] == 'ENDMDL' ):
                    print( line.strip() )
                else:
                    pass # ignoring all other lines

        return 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser( description=__doc__ )
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-a', '--hetatm', dest='hetatm', required=False, help='show HETATM lines', default=False, action='store_true' )
    parser.add_argument( '-t', '--ter', dest='ter', required=False, help='show TER lines', default=False, action='store_true' )
    parser.add_argument( '-e', '--end', dest='end', required=False, help='show END lines', default=False, action='store_true' )
    parser.add_argument( '-m', '--model', dest='model', required=False, help='show MODEL lines', default=False, action='store_true' )
    main = pdb_atom_hetatm_only( args=parser.parse_args() )
    main.run()
