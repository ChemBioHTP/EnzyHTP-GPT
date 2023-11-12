prompt_skeleton = (
        """Now you are a natural language converter that convert natural language into a pattern defined below. You will be answering questions in the format of "Query:[the natural language]" and 
        you will answer in a format of "Answer:[the converted pattern]". 
        If the input makes no sense to the pattern syntax, please output "Error".
        Here is the pattern defination:
        pattern: the pattern that defines the mutation (see syntax below)
        *Pattern Syntax:*
            "mutant_1,mutant_2,mutant_3,..."
            The top layer of the mutation_pattern specify mutants with comma seperated patterns
            In the pattern of each mutant, there could be more than one sections, but if multiple
            sections are used, {} is needed to group those sections.
            "{section_a1,section_a2,section_a3},{section_b1,section_b2,section_b3},..."
            Each section can be one of the format below:
            1. direct indication                    : XA###Y
            2. random M, N-point mutation in a set  : r:N[mutation_esm_patterns]*M
                                                        or r:NR[mutation_esm_patterns]*MR
                                                        (N and M are int,
                                                        R stands for allowing repeating mutations in randomization)
            3. all mutation in a set: a             : a:[mutation_esm_patterns]
                                                        or a:M[mutation_esm_patterns]
                                                        (M stands for force mutate each position so that
                                                        no mutation on any position is not allowed)

            The mutation_esm_patterns is seperated by comma and each describes 2 things:
            1. position_pattern: a set of positions
                                (check selection syntax in .mutation_pattern.position_pattern)
                                NOTE: all non polypeptide part are filtered out.
            2. target_aa_pattern: a set of target mutations apply to all positions in the current set
                                (check syntax in .mutation_pattern.target_aa_pattern)
            The two pattern are seperated by ":" and a mutation_esm_patterns looks like:
            "position_pattern_0:target_aa_pattern_0, ..."

            *In 2&3 the pattern may indicate a mutant collection, if more than one mutant collection
            are indicated in the same {}, all combination of them is considered.

            Overall an example of pattern will be:
            "{RA154W, DA11G}, r:2[resi 289 around 4 and not resi 36:larger, proj(id 1000, id 2023, positive, 10):more_negative_charge]*100"
            * here proj() is a hypothetical selection function

        selection syntax in .mutation_pattern.position_pattern:
        a PyMol-like syntax to select residue positions. Find the PyMol selection syntax at https://pymolwiki.org/index.php/Selection_Algebra

        syntax in .mutation_pattern.target_aa_pattern:
        The pattern is compose by keywords connected by logical operators:
                            (current supported keywords)
                            self:       the AA itself
                            all:        all 20 canonical amino acid (AA)
                            larger:     AA that is larger in size according to
                                        enzy_htp.chemical.residue.RESIDUE_VOLUME_MAPPER
                            smaller:    AA that is smaller in size
                            similar_size_20: AA that similar is size (cutoff: 20 Ang^3)
                            charge+:    AA that carry more formal positive charge
                            charge-:    AA that carry less formal positive charge
                            charge+1:   AA that carry 1 more positive charge
                            charge-1:   AA that carry 1 less positive charge
                            neutral:    AA that is charge neutral
                            positive:   AA that have positive charge
                            negative:   AA that have negative charge
                            {3-letter}: the AA of the 3-letter name

        If you understand want you need to do, I will start giving you real responses. Query: {question}\nAnswer:"""
    )