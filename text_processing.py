# Lauryn Anderson
# MIT License
import numpy as np
import spacy
from spacy.lang.en import English
import pandas

nlp = spacy.load('en_core_web_sm')
spacy_model = English()


def preprocess_text(text):

    # tokenize and preprocess text
    doc = nlp(text)
    doc = retokenize_entities(doc)
    tokens = pandas.DataFrame(doc, columns=['token'])
    if len(tokens) < 1:
        return tokens
    tokens['pos'] = tokens.apply(lambda row: row.token.tag_, axis=1)
    tokens['biluo'] = tokens.apply(lambda row: row.token.ent_iob_, axis=1)

    # identify target parts of speech

    targets = {
        'nouns': tokens[tokens['pos'] == 'NN'].copy(),
        'plural_nouns': tokens[tokens['pos'] == 'NNS'].copy(),
        'proper_nouns': tokens[tokens['pos'] == 'NNP'].copy(),
        'adjectives': tokens[tokens['pos'] == 'JJ'].copy(),
        'adverbs': tokens[tokens['pos'] == 'RB'].copy(),
        'numbers': tokens[tokens['pos'] == 'CD'].copy(),
        'exclamations': tokens[tokens['pos'] == 'UH'].copy(),
        'base_verbs': tokens[tokens['pos'] == 'VB'].copy(),
        'gerund_verbs': tokens[tokens['pos'] == 'VBG'].copy(),
    }
    targets['nouns']['prompt'] = 'Noun'
    targets['plural_nouns']['prompt'] = 'Plural Noun'
    targets['proper_nouns']['prompt'] = 'Proper Noun'
    targets['adjectives']['prompt'] = 'Adjective'
    targets['adverbs']['prompt'] = 'Adverb'
    targets['numbers']['prompt'] = 'Number'
    targets['exclamations']['prompt'] = 'Exclamation'
    targets['base_verbs']['prompt'] = 'Verb'
    targets['gerund_verbs']['prompt'] = 'Verb Ending in "ing"'

    # select tokens to be blanked
    # one from each part of speech plus a subset
    blanks_by_pos = []

    for _, target in targets.items():
        if len(target) > 0:
            blanks_by_pos.append(target.sample(1))
            blanks_by_pos.append(target.sample(frac=0.3))

    if len(blanks_by_pos) > 0:
        # update token dataframe with selected blanks
        blanks = pandas.concat(blanks_by_pos).drop_duplicates()
        tokens = pandas.merge(tokens, blanks, 'left', validate='one_to_one')
    else:
        tokens['prompt'] = np.nan

    print(tokens)
    return tokens


def retokenize_entities(doc):

    for ent in reversed(doc.ents):
        # retokenize entities in reverse order
        # so that the indices are not displaced as the operation takes place
        with doc.retokenize() as retokenizer:
            retokenizer.merge(
                doc[ent.start:ent.end],
                attrs={"LEMMA": str(doc[ent.start:ent.end])}
            )
    return doc
