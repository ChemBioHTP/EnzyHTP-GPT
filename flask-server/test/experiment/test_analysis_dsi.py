import os

from experiment.analysis import _domain_sequences_to_residue_ranges
from enzy_htp import PDBParser

sp = PDBParser()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = f"{SCRIPT_DIR}/data"

def test_domain_sequences_to_residue_ranges():
    stru = sp.get_structure(f"{DATA_DIR}/test.pdb")
    domain1, domain2 = _domain_sequences_to_residue_ranges(
        stru=stru,
        domain1_sequence="MSTPSLIPSGVHEVLAKYKDGNYVDGWAELWDKSKGDRLPWDRGFPNPALEDTLIQKRAIIGGPLGQDAQGKTYRKKALVPGCGRGVDVLLLASFGYDAYGLEYSATAVDV",
        domain2_sequence="HPGEEIPYDASRQCQFDSSKAPSAQGLERVAYWQPERTHEVGKNEKGEVQDRVSIWQRPPQSSL",
    )
    assert domain1 == [("A", 1), ("A", 111)]
    assert domain2 == [("A", 225), ("A", 288)]
