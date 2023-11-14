from flask import Flask, request, jsonify
import openai
import config
import enzy_htp.structure
import enzy_htp.mutation.api as mapi
import enzy_htp.mutation.mutation_pattern.api as pattern_api

app = Flask(__name__)

@app.route("/api/generate_pattern", methods=["POST"])
def generate_pattern():
    mutation_request = request.json['mut_request']
    api_key = request.json['api_key']

    prompt = ""
    prompt += config.prompt_skeleton
    prompt += f"Query:{mutation_request}\nAnswer:"
    
    openai.api_key = api_key

    # TODO: how to improve prompt in config.py?
    try:
        completions = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=70,
            frequency_penalty=-0.5,
            temperature=0.01,
        )
        message = completions.choices[0].text
    except Exception as e:
        raise Exception(f'API Error: {str(e)}')

    return jsonify({"mutations": message})

def generate_muts(file, pattern):
    sp = enzy_htp.structure.PDBParser()
    stru = sp.get_structure(file.name)

    # checks to make sure mutation is valid before continuing
    try:
        mutations = pattern_api.decode_mutation_pattern(stru, pattern)
    except pattern_api.InvalidMutationPatternSyntax as e:
        raise Exception(f'Invalid mutation: {str(e)}')

    res = []
    # mutates the PDB file with PyMOL
    for mut in mutations:
        try:
            mutant_stru = mapi.mutate_stru(stru, mut, engine="pymol")
            res_file = sp.get_file_str(mutant_stru)
        except Exception as e:
            raise Exception(f'API Error: {str(e)}')
        name_tag = ""
        for single_mut in mut:
            name_tag += str(single_mut) + "_"
        name_tag = name_tag[:-1]
        res.append((res_file, name_tag))

    return res

if __name__ == "__main__":
    app.run(debug=True)