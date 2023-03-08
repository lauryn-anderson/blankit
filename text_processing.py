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
    tokens = pandas.DataFrame(nlp(text), columns=['token'])
    if len(tokens) < 1:
        return tokens
    tokens['pos'] = tokens.apply(lambda row: row.token.pos_, axis=1)

    # identify target parts of speech
    nouns = tokens[tokens['pos'] == 'NOUN'].copy()
    adjectives = tokens[tokens['pos'] == 'ADJ'].copy()
    adverbs = tokens[tokens['pos'] == 'ADV'].copy()
    verbs = tokens[tokens['pos'] == 'VERB'].copy()

    # select tokens to be blanked
    # one from each part of speech plus a subset
    blanks_by_pos = []

    if len(nouns) > 0:
        nouns['prompt'] = 'Noun'
        blanks_by_pos.append(nouns.sample(1))
        blanks_by_pos.append(nouns.sample(frac=0.3))

    if len(adjectives) > 0:
        adjectives['prompt'] = 'Adjective'
        blanks_by_pos.append(adjectives.sample(1))
        blanks_by_pos.append(adjectives.sample(frac=0.3))

    if len(adverbs) > 0:
        adverbs['prompt'] = 'Adverb'
        blanks_by_pos.append(adverbs.sample(1))
        blanks_by_pos.append(adverbs.sample(frac=0.3))

    if len(verbs) > 0:
        verbs['prompt'] = 'Verb'
        blanks_by_pos.append(verbs.sample(1))
        blanks_by_pos.append(verbs.sample(frac=0.3))

    if len(blanks_by_pos) > 0:
        # update token dataframe with selected blanks
        blanks = pandas.concat(blanks_by_pos).drop_duplicates()
        tokens = pandas.merge(tokens, blanks, 'left', validate='one_to_one')
    else:
        tokens['prompt'] = np.nan

    print(tokens)
    return tokens


# preprocess_text('In natural language processing, we boldly approach interesting problems.')
