#! python3
# -*- encoding: utf-8 -*-
'''
@File    :   prompts.py
@Created :   2024/09/14 12:59
@Author  :   Ran, Xinchun; Stull, Sebastian
@Version :   2.0
@Contact :   xinchun.ran@vanderbilt.edu; sebastian.l.stull@vanderbilt.edu
'''

# Here put the import lib.
prompt_skeleton = """Now you are a natural language to EnzyHTP mutation syntax converter that converts natural language into a pattern defined below. 
You will be answering questions in the format of "Query: [the natural language]" and you will answer in the format of "Answer: [the converted pattern]",
while the text "Answer: " is not required to be included in your response. 
       
Here is the pattern reflection table definition:

| Keyword                                   | EnzyHTP Syntax                                           |
|-------------------------------------------|----------------------------------------------------------|
| Wild type                                 | WT                                                       |
| Random                                    | r                                                        |
| Single-point                              | 1                                                        |
| Double-point                              | 2                                                        |
| Three-point                               | 3                                                        |
| Mutant                                    | {mutation}                                               |
| Within 5Å of                              | around 5                                                 |
| Substrate                                 | resn LIG                                                 |
| Cofactor XX                               | resn   XX                                                |
| Binding pocket                            | byres resn LIG                                           |
| Generate X mutants                        | *X                                                       |
| Generate X double point mutants           | *2*X                                                     |
| Chain A                                   | chain A                                                  |
| Chain B                                   | chain B                                                  |
| Chain D                                   | chain D                                                  |
| mutation Y107 on Chain D to H amino acid  | YD107B                                                   |
| Increase                                  | smaller                                                  |
| Decrease                                  | larger                                                   |
| Positive charges                          | charge+                                                  |
| Negative charges                          | charge-                                                  |
| Neutral amino acids                       | neutral                                                  |
| Homologous dimeric protein                | byres chain A around 5.0 and chain B                     |
| Dimer interface                           | byres chain A around 5.0 and chain B                     |
| all mutate                                | a                                                        |
| Not mutate all                            | all not self                                             |
| Distal residues                           | byres all and not (byres resn LIG around 30 or resn LIG) |


The mutation_esm_patterns are separated by a comma and each describes 2 things:
1. position_pattern: a set of positions
                    (check selection syntax in .mutation_pattern.position_pattern)
                    NOTE: All polypeptide parts are filtered out.
2. target_aa_pattern: a set of target mutations apply to all positions in the current set
                    (check the syntax in .mutation_pattern.target_aa_pattern)
The two pattern are separated by ":" and a mutation_esm_patterns looks like:
"position_pattern_0:target_aa_pattern_0, ..."

*In 2&3 the pattern may indicate a mutant collection, if more than one mutant collection
are indicated in the same {}, all combination of them is considered.

The mutation_esm_patterns are separated by a comma and each describes 2 things:
1. position_pattern: a set of positions
                    (check selection syntax in .mutation_pattern.position_pattern)
                    NOTE: All polypeptide parts are filtered out.
2. target_aa_pattern: a set of target mutations apply to all positions in the current set
                    (check the syntax in .mutation_pattern.target_aa_pattern)
The two pattern are separated by ":" and a mutation_esm_patterns looks like:
"position_pattern_0:target_aa_pattern_0, ..."

*In 2&3 the pattern may indicate a mutant collection, if more than one mutant collection
are indicated in the same {}, all combination of them is considered.

Overall examples of a pattern will be:
1.  "{RA154W, DA11G}, r:2[resi 289 around 4 and not resi 36:larger, proj(id 1000, id 2023, positive, 10):more_negative_charge]*100".
2. And another example will be "Keep it as a wild type". The answer can be [[(None,' WT', None, None)]] or "WT"
3.  "Perform random mutagenesis on amino acids within 5Å of the LIG substrate binding pocket. Generate 20 double-point-mutation mutants total."  The output should be: "r:2[byres resn LIG around 5:all not self]*20"
4. "Generate a mutant with double-point mutation: G83H and H36E with chain A and Chain B respectively ". The output should be " {GA83H, HB36E}"
5. "Generate 20 random single-point-mutation mutants of the target protein." "The output should be "r:1[all:all not self]*20""
6. "Mutate residues using the protein with the LIG substrate near the binding pocket, defined as residues within 3 Å of LIG, to introduce more positive charges to the pocket. Not all residues need to be force mutated." The output should be "a:[byres resn LIG around 3:charge+]"
7. "For the protein with the LIG substrate, mutate residues near the binding pocket (defined as within 5Å of LIG) to increase the pocket volume. Some residues may remain unmutated." The output should be "a:[byres resn LIG around 5:smaller]"
8. "Generate 5 random mutants with single-point mutation using the protein with the LIG substrate to introduce more negative charges to distal residues, defined as over 30 Å away from the substrate." The output should be "r:1[byres all and not (byres resn LIG around 30 or resn LIG):charge-]*5"
9. "Randomly generate 3 double mutants by mutating residues at the dimer interface to smaller amino acids for a homologous dimeric protein." The output should be "r:2[byres chain A around 5.0 and chain B:smaller]*3"
10: "For a homologous dimeric protein, randomly generate 4 three-point-mutation mutants by mutating residues at the dimer interface to neutral amino acids." The output should be "r:3[byres chain A around 5.0 and chain B:neutral]*4"
11:"Perform 10 random double-point mutations on amino acids within 5 Å of the LIG substrate binding pocket, resulting in 10 different double mutants. Allow repeated single mutations." the output should be "r:2R[byres resn LIG around 5:all not self]*20

Query: ${question}
Answer: """