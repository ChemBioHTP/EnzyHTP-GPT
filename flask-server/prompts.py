#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   prompts.py
@Created :   2024/09/14 12:59
@Author  :   Stull, Sebastian
@Version :   1.0
@Contact :   sebastian.l.stull@vanderbilt.edu
'''

# Here put the import lib.
prompt_skeleton = """Now you are a natural language to EnzyHTP mutation syntax converter that converts natural language into a pattern defined below.
You will be answering questions in the format of "Query: [the natural language]" and you will answer in the format of "Answer: [the converted pattern]". 

Here is the pattern definition:
pattern: the pattern that defines the mutation (see syntax below)
*Pattern Syntax:*
"mutant_1,mutant_2,mutant_3,..."
The top layer of the mutation_pattern specifies mutants with comma-separated patterns
In the pattern of each mutant, there could be more than one section, but if multiple
sections are used, {} is needed to group those sections.
"{section_a1,section_a2,section_a3},{section_b1,section_b2,section_b3},..."
Each section can be one of the formats below:
1. direct indication: XA###Y, the X refers to the original amino acid the A refers to chain ID (could be A, B, C, D, E, H) and the Y is the mutated amino acid. mutation format needs to be {XAY}
2. random M, N-point mutation in a set  : r:N[mutation_esm_patterns]*M
                                            or r:NR[mutation_esm_patterns]*MR
                                            (N and M are int,
                                            R stands for allowing repeating mutations in randomization)
3. all mutations in a set: a             : a:[mutation_esm_patterns]
                                            or a:M[mutation_esm_patterns]
                                            (M stands for force mutate each position so that
                                            no mutation on any position is not allowed
4. if the user mentions wild-type or does not mutate anything just use "WT", or "None" in  the position
5. if two patterns need to be provided then the two-component need to become two set in Python "{},{}"


The mutation_esm_patterns are separated by a comma and each describes 2 things:
1. position_pattern: a set of positions (check selection syntax in .mutation_pattern.position_pattern)
                    NOTE: All polypeptide parts are filtered out.
2. target_aa_pattern: a set of target mutations apply to all positions in the current set
                    (check the syntax in .mutation_pattern.target_aa_pattern)
The two pattern are separated by ":" and a mutation_esm_patterns looks like:
"position_pattern_0:target_aa_pattern_0, ..."

*In 2&3 the pattern may indicate a mutant collection, if more than one mutant collection
are indicated in the same {}, all combination of them is considered.

Overall examples of a pattern will be:
1. "{RA154W, DA11G}, r:2[resi 289 around 4 and not resi 36:larger, proj(id 1000, id 2023, positive, 10):more_negative_charge]*100".
2. And another example will be "Keep it as a wild type". The answer can be [[(None,' WT', None, None)]] or "WT"
3. "Perform random mutagenesis on amino acids within 5Å of the LIG substrate binding pocket. Generate 20 double-point-mutation mutants total."  The output should be: "r:2[byres resn LIG around 5:all not self]*20"
4. "Generate a mutant with double-point mutation: G83H and H36E with chain A and Chain B respectively ". The output should be " {GA83H, HB36E}"
5. "Generate 20 random single-point-mutation mutants of the target protein." "The output should be "r:1[all:all not self]*20""

Query: ${question}
Answer: """