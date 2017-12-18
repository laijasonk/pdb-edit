#!/usr/bin/env python3.4

"""Keep only first alternative/unresolved atom in PDB file (labeled with A on column 17)."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.github.com/jklai'

class pdb_force_single_alternative_atom( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None

        return

    def run( self ):

        """The main function."""

        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )

        # loop through every line of input PDB and identify and fix alternative atom lines
        prev_aa_line = '' # track previous line to identify repeat atoms
        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:

                if line[0:4] == 'ATOM' or line[0:6] == 'HETATM' or line[0:6] == 'ANISOU':
                    new_line = self.keep_repeat_atom_line( line, prev_aa_line )
                    if new_line:
                        print( new_line.strip() )
                    else:
                        pass # do not keep this repeat atom line
                else:
                    print( line.strip() ) # script keeps all other lines intact

                prev_aa_line = line

        return

    def keep_repeat_atom_line( self, in_line, prev_line ):

        """Return cleaned atom lines otherwise return false"""

        out_line = in_line
        try:
            if in_line[26] != ' ': 
                return False # found a modified atom, so ignore it
            elif in_line[13:16] == prev_line[13:16] and in_line[16] != ' ' and in_line[16] != 'A':
                return False # found a repeat atom, so ignore it
            else:
                # remove unnecessary A/B/C/etc at columns 17 aad 27
                out_line = out_line[:16] + ' ' + out_line[17:]
                out_line = out_line[:26] + ' ' + out_line[27:]
        except:
            raise ValueError( 'Incomplete ATOM or HETATM line.' )
        
        return out_line
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )

    # command line execution
    main = pdb_force_single_alternative_atom( args=parser.parse_args() )
    main.run()
