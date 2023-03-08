# Lauryn Anderson
# MIT License

import spacy
from spacy.lang.en import English

import pandas

nlp = spacy.load('en_core_web_sm')
spacy_model = English()


def preprocess_text(text):

    # tokenize and preprocess text
    tokens = pandas.DataFrame(nlp(text), columns=['token'])
    tokens['pos'] = tokens.apply(lambda row: row.token.pos_, axis=1)

    # identify target parts of speech
    nouns = tokens[tokens['pos'] == 'NOUN']
    adjectives = tokens[tokens['pos'] == 'ADJ']
    adverbs = tokens[tokens['pos'] == 'ADV']

    # select tokens to be blanked
    # one from each part of speech plus a subset
    blanks_by_pos = [
        nouns.sample(1), adjectives.sample(1), adverbs.sample(1),
        nouns.sample(frac=0.3), adjectives.sample(frac=0.3), adverbs.sample(frac=0.3),
    ]
    blanks = pandas.concat(blanks_by_pos).drop_duplicates()
    blanks['blank'] = True

    # update token dataframe with selected blanks
    tokens = pandas.merge(tokens, blanks, 'left', validate='one_to_many')
    print(tokens)


preprocess_text('In natural language processing, we boldly approach interesting problems.')
