from flask import Flask, render_template, request
import spacy
import networkx as nx
import matplotlib


matplotlib.use('Agg')


import matplotlib.pyplot as plt


app = Flask(__name__)


nlp = spacy.load("en_core_web_sm")

def analyze_paragraph(paragraph):
    
    doc = nlp(paragraph)

    
    named_entities = []
    parts_of_speech = []

    
    G = nx.Graph()


    for sent in doc.sents:
        # Named Entities
        sentence_named_entities = []
        for ent in sent.ents:
            sentence_named_entities.append(f"{ent.text} ({ent.label_})")
        named_entities.append(sentence_named_entities)

        # Parts of Speech
        sentence_parts_of_speech = []
        for token in sent:
            sentence_parts_of_speech.append(f"{token.text} ({token.pos_})")
        parts_of_speech.append(sentence_parts_of_speech)

        # dependency graph
        for token in sent:
            G.add_node(token.text)
            if token.dep_ != "punct":
                G.add_edge(token.text, token.head.text, label=token.dep_)

  
    pos = nx.spring_layout(G, seed=42)
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Specify the path to save the image in the current directory
    image_path = "dependency_graph.png"
    plt.savefig(image_path)


    return named_entities, parts_of_speech, image_path

@app.route("/", methods=["GET", "POST"])
def index():
    paragraph = ""
    dependency_graph_path = None
    named_entities = []
    parts_of_speech = []

    if request.method == "POST":
        paragraph = request.form.get("paragraph")
        if paragraph:
            named_entities, parts_of_speech, dependency_graph_path = analyze_paragraph(paragraph)

    return render_template("index.html", paragraph=paragraph, dependency_graph_path=dependency_graph_path, named_entities=named_entities, parts_of_speech=parts_of_speech)

if __name__ == "__main__":
    app.run(debug=True)
