#!/usr/bin/env python3.4

"""Keep only first alternative/unresolved atom in PDB file (labeled with A on column 17)."""

import argparse

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_force_single_alternative_atom( object ):
    def __init__( self, args=None ):
        """The class constructor."""
        self.pdb = args.pdb if args is not None else None
        return

    def run( self ):
        """The main function."""
        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )

        prev_aa_line = '' # track previous line to identify repeat atoms
        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:
                if line[0:4] == 'ATOM' or line[0:6] == 'HETATM':
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
                out_line = out_line[:16] + ' ' + out_line[17:] # remove unnecessary A/B/C/etc at column 17
                out_line = out_line[:26] + ' ' + out_line[27:] # remove unnecessary A/B/C/etc at column 27
        except:
            raise ValueError( 'Incomplete ATOM or HETATM line.' )
        
        return out_line
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser( description=__doc__ )
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    main = pdb_force_single_alternative_atom( args=parser.parse_args() )
    main.run()
