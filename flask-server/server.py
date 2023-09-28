from flask import Flask, request, jsonify
import openai
import config

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
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=70,
            frequency_penalty=-0.5,
            temperature=0.2,
        )
        message = completions.choices[0].text
    except Exception as e:
        raise Exception(f'API Error: {str(e)}')

    #TODO: pass this response into EnzyHTP for further processing rather than returning it
    return jsonify({"mutations": message})

if __name__ == "__main__":
    app.run(debug=True)