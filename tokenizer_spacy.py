import spacy
from spacy import displacy

def tokenize(txt):
    nlp = spacy.load("ja_ginza")
    #filter_words =["Dish","Food_Other","Flora_Part","Compound","Drug","Flora"]
    filter_words =["Food_Other","Flora_Part","Compound","Drug","Flora"]
    #nlp = spacy.load("ja_ginza_electra")
    doc = nlp(txt)
    words =[]
    for ent in doc.ents:
        
        #print(ent.text, ent.label_, ent.start_char, ent.end_char)
        if ent.label_ in filter_words:
            words.append(ent.text)
            print(ent.text)
    return words
#displacy.render(doc, style="ent", options={"compact":True},  jupyter=True)


