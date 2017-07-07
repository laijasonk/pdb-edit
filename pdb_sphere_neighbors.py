#!/usr/bin/env python2.7

"""Output amino acid residues (not HETATM) with at least one heavy atom around the input xyz coordinates."""

import argparse, sys, math

__author__ = 'Jason K Lai'
__contact__ = 'http://www.jasonlai.com/'

class pdb_sphere_neighbors( object ):

    def __init__( self, args=None ):

        """The class constructor."""

        self.pdb = args.pdb if args is not None else None
        self.xcoord = args.xcoord if args is not None else None
        self.ycoord = args.ycoord if args is not None else None
        self.zcoord = args.zcoord if args is not None else None
        self.threshold = args.threshold if args is not None else None

        return

    def run( self ):

        """The main function."""

        if self.pdb is None:
            raise ValueError( 'Missing input PDB.' )
        if self.xcoord is None or self.ycoord is None or self.zcoord is None:
            raise ValueError( 'Incomplete XYZ coordinates.' )
        if self.threshold is None: self.threshold = 8

        # parse input pdb into a Python list with one atom per element
        try:
            pdb_list = self.pdb_to_list( open( self.pdb, 'rt' ) )
        except:
            raise ValueError( 'Invalid input PDB file.' )

        # identify residues in the input pdb that are near the input coordinates
        try:
            nearby_res_from_coord = self.find_nearby_residues( pdb_list )
        except:
            raise ValueError( 'Please clean input PDB file (e.g. amino acid index numbering).' )

        # loop through every line in the input pdb and only show residues previously identified
        with open( self.pdb, 'r' ) as pdb_handle:
            for line in pdb_handle:

                if self.show_line( line, nearby_res_from_coord ):
                    print( line.strip() )
                else:
                    pass # line does contain correct residue index
        
        return

    def pdb_to_list( self, pdb_handle ):

        """Convert input pdb file handle to a list of atoms (input PDB must have no breaks in AA numbering)."""

        out_list = []
        residue_count = -1
        previous_number = 0

        # run through every line in the pdb and parse it into a list if it is a heavy atom
        for line in pdb_handle:
            if line[0:4] == 'ATOM' and not line[13] == 'H':
                residue_number = int( line[23:26] )

                if not residue_number == previous_number:
                    residue_count = residue_count + 1
                    out_list.append( [] )
                else:
                    pass

                chain = str( line[21] )
                amino_acid = line[17:20]
                x = float( line[30:38] )
                y = float( line[38:46] )
                z = float( line[46:54] )

                out_list[ residue_count ].append( [ residue_number, chain, amino_acid, x, y, z ] )
                previous_number = residue_number

        return out_list

    def find_nearby_residues( self, pdb_list ):

        """Return list of residue indices that are near."""

        nearby_res_indexes = []
        for res_index in range( len( pdb_list ) ):
            distance = self.res_dist_from_coord( res_index, pdb_list )

            if distance < self.threshold:
                nearby_res_indexes.append( pdb_list[ res_index ][0][0] )

        return nearby_res_indexes

    def res_dist_from_coord( self, res_index, pdb_list ):

        """Return distance of a specific residue from the input XYZ coordinates."""

        shortest_distance = sys.maxsize

        # find all distances between an input atom and input XYZ that are within threshold
        for idx in range( len( pdb_list[res_index] ) ):

            x1 = float( pdb_list[res_index][idx][3] )
            y1 = float( pdb_list[res_index][idx][4] )
            z1 = float( pdb_list[res_index][idx][5] )

            x2 = float( self.xcoord )
            y2 = float( self.ycoord )
            z2 = float( self.zcoord )

            distance = math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2 )

            if distance < shortest_distance:
                shortest_distance = distance

        return shortest_distance
    
    def show_line( self, in_line, idx_list ):

        """Find and return matches according to input option flags."""

        if in_line[0:4] == 'ATOM':

            aa_idx = int( in_line[23:26] )
            if aa_idx in idx_list:
                return in_line
            else:
                pass # residue index not in specified list

        else:
            pass # not an ATOM coordinate line
        
        return False
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser( description=__doc__ )

    # command line option flags
    parser.add_argument( '-p', '--pdb', dest='pdb', required=True, help='input pdb file (including path if necessary)', type=str )
    parser.add_argument( '-x', '--xcoord', dest='xcoord', required=True, help='x coordinate of sphere center', type=str )
    parser.add_argument( '-y', '--ycoord', dest='ycoord', required=True, help='y coordinate of sphere center', type=str )
    parser.add_argument( '-z', '--zcoord', dest='zcoord', required=True, help='z coordinate of sphere center', type=str )
    parser.add_argument( '-t', '--threshold', dest='threshold', required=False, default=8, help='distance threshold in Angstroms (default=6)', type=float )

    # command line execution
    main = pdb_sphere_neighbors( args=parser.parse_args() )
    main.run()
