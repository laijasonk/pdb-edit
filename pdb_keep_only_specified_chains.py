#!/usr/bin/env python3.4

"""Only keep ATOM or HETATM lines from specified chain identifiers (single or multiple)."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_keep_only_specified_chains( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None
        self.chains = args.chains if args is not None else None
        
        return

    def run( self ):

        """The main function."""

        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.chains is None:
            raise ValueError( 'Missing input chain identifiers.' )

        # loop through every line of input pdb and keep only lines with specified chain identifiers
        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:

                if line[0:4] == 'ATOM' or line[0:6] == 'HETATM' or line[0:3] == 'TER':
                    if self.line_contains_chain( line, self.chains ):
                        print( line.strip() )
                    else:
                        pass # did not find the correct chain identifier on this line
                else:
                    pass # ignoring all non ATOM or HETATM lines

        return 
    
    def line_contains_chain( self, in_line, in_chains ):

        """Check if the input line contains the specified chain(s)."""

        try:
            # standard PDB syntax has the chain on column 22 (21 when index starts at 0)
            for chain in in_chains:
                if len( in_line ) > 21:

                    if in_line[21] == chain:
                        return True
                    else:
                        pass # did not contain correct chain identifier

                else:
                    pass # ignore if line isn't even 21 characters long
        except:
            raise ValueError( 'Invalid ATOM or HETATM line.' )
            
        return False
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-c', '--chains', dest='chains', required=True, help='string of all chain identifiers to keep (e.g. "ADF")', type=str )

    # command line execution
    main = pdb_keep_only_specified_chains( args=parser.parse_args() )
    main.run()
