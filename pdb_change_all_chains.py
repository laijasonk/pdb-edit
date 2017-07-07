#!/usr/bin/env python3.4

"""Changes every line in the PDB file to a single specified chain character."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_change_all_chains( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None
        self.chain = args.chain if args is not None else None
        return

    def run( self ):
        """The main function."""
        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.chain is None:
            raise ValueError( 'Missing input chain identifier.' )
        if len( self.chain ) > 1:
            raise ValueError( 'Chain identifier must be a single character.' )

        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:
                if line[0:4] == 'ATOM' or line[0:6] == 'HETATM':
                    print( self.force_line_to_chain( line, self.chain ).strip() )
                else:
                    print( line.strip() ) # script keeps all other lines intact

        return 
    
    def force_line_to_chain( self, in_line, in_chain ):
        """Force input line to be chain."""
        out_line = ''
        try:
            # standard PDB syntax has the chain on column 22
            out_line = in_line[ :21 ] + str( in_chain ) + in_line[ 22: ]
        except:
            raise ValueError( 'Incomplete ATOM or HETATM line.' )
            
        return out_line
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-c', '--chain', dest='chain', required=True, help='single character chain identifier', type=str )

    # command line execution
    main = pdb_change_all_chains( args=parser.parse_args() )
    main.run()
