# Lauryn Anderson
# MIT License
import numpy as np
import spacy
from spacy.lang.en import English
import pandas

from constants import masc_set, fem_set

nlp = spacy.load('en_core_web_sm')
spacy_model = English()
nlp.add_pipe('coreferee')


def preprocess_text(text):

    # tokenize and preprocess text
    doc = nlp(text)
    gender_identities = extract_gender(doc)
    doc = retokenize_entities(doc)
    tokens = pandas.DataFrame(doc, columns=['token'])

    if len(tokens) < 1:
        return tokens
    tokens['pos'] = tokens.apply(lambda row: row.token.tag_, axis=1)
    tokens['ent'] = tokens.apply(lambda row: row.token.ent_type_, axis=1)

    # select tokens to be blanked
    targets = identify_targets(tokens)

    # evaluate people tags to detect preferred pronouns
    targets['people'] = resolve_coreferences(targets['people'], gender_identities)

    blanks_by_pos = []

    for _, target in targets.items():
        # choose one blank from each part of speech plus a subset
        if len(target) > 0:
            blanks_by_pos.append(target.sample(1))
            blanks_by_pos.append(target.sample(frac=0.3))

    if len(blanks_by_pos) > 0:
        # update token dataframe with selected blanks
        blanks = pandas.concat(blanks_by_pos).drop_duplicates()
        tokens = pandas.merge(tokens, blanks, 'left', validate='one_to_one')
    else:
        tokens['prompt'] = np.nan

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
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


def identify_targets(tokens):

    # identify target entities

    targets = {
        'people': tokens[tokens['ent'] == 'PERSON'].copy(),
        'orgs': tokens[tokens['ent'] == 'ORG'].copy(),
        'places': tokens[tokens['ent'] == 'GPE'].copy(),
    }
    targets['people']['prompt'] = "Person's Name"
    targets['orgs']['prompt'] = 'Organization'
    targets['places']['prompt'] = 'Place'

    # identify target parts of speech

    pos_tokens = tokens.drop(index=tokens[tokens['ent'] != ''].index)
    targets.update({
        'nouns': pos_tokens[pos_tokens['pos'] == 'NN'].copy(),
        'plural_nouns': pos_tokens[pos_tokens['pos'] == 'NNS'].copy(),
        'proper_nouns': pos_tokens[pos_tokens['pos'] == 'NNP'].copy(),
        'adjectives': pos_tokens[pos_tokens['pos'] == 'JJ'].copy(),
        'adverbs': pos_tokens[pos_tokens['pos'] == 'RB'].copy(),
        'numbers': pos_tokens[pos_tokens['pos'] == 'CD'].copy(),
        'exclamations': pos_tokens[pos_tokens['pos'] == 'UH'].copy(),
        'base_verbs': pos_tokens[pos_tokens['pos'] == 'VB'].copy(),
        'gerund_verbs': pos_tokens[pos_tokens['pos'] == 'VBG'].copy(),
    })
    targets['nouns']['prompt'] = 'Noun'
    targets['plural_nouns']['prompt'] = 'Plural Noun'
    targets['proper_nouns']['prompt'] = 'Proper Noun'
    targets['adjectives']['prompt'] = 'Adjective'
    targets['adverbs']['prompt'] = 'Adverb'
    targets['numbers']['prompt'] = 'Number'
    targets['exclamations']['prompt'] = 'Exclamation'
    targets['base_verbs']['prompt'] = 'Verb'
    targets['gerund_verbs']['prompt'] = 'Verb Ending in "ing"'

    return targets


def extract_gender(doc):
    dic = {}
    for chain in doc._.coref_chains:
        genders = set()
        for mention in chain:
            token = doc[mention.root_index]
            for gender in token.morph.get('Gender'):
                genders.add(gender)
        # check if gender is uniformly masc/fem
        if genders == masc_set:
            dic[chain] = "Person's Name (he/him)"
        if genders == fem_set:
            dic[chain] = "Person's Name (she/her)"
    return dic


def resolve_coreferences(people, gender_identities):
    for index, person in people.iterrows():
        for chain in person.token._.coref_chains:
            if chain in gender_identities:
                person['prompt'] = gender_identities[chain]
    return people
