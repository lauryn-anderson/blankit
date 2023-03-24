# Notes on the Research Process

After creating the initial naive implementation, 
I had to identify shortcomings and techniques to 
improve the Mad Lib generator. 

## Fine-Grained Parts of Speech

In the naive implementation, I use the basic, 
coarse-grained part-of-speech tagging provided in 
SpaCy. This library also includes a more fine-
grained POS tagger based on the Penn Treebank 
Project dataset. 

The Penn Treebank operated from 1989 to 1996, 
producing more than 7 million words of English 
POS-tagged text across a wide range of material.
It categorises words into 36 detailed POS tags, 
capturing basic inflectional properties of verbs 
and nouns. These tags are clearly defined in 
this document:

Beatrice Santorini. 1990. _Part-of-speech tagging 
guidelines for the penn treebank project._ 
Technical report MS-CIS-90-47. University of 
Pennsylvania.

I analysed this document to identify possibilities 
for improvement using this more specific 
categorization. Even when the category is 
essentially the same as the simpler POS tagger, 
these tags will be more refined because of sub-
categorization. For example, using the adjective 
tag from this dataset will exclude comparative 
and superlative adjectives. 

### Adjectives

The Penn Treebank tags differentiate adjectives
(including ordinals) `JJ` from comparative `JJR` 
and superlative `JJS` adjectives. 

The same is true for adverbs (`RB`, `RBR`, `RBS`).

### Numbers

The Penn Treebank tags pull out cardinal numbers 
into their own tag, `CD`. This is a tag in the 
original Mad Libs. 

### Interjections

Also known as exclamations, interjections are 
tagged with `UH`. This is a tag in the original 
Mad Libs.

### Nouns

Nouns are split into singular/mass nouns `NN` or 
plural nouns `NNS`. However, there is no distinc-
tion between singular and mass nouns. 

Proper nouns are tagged as `NP` for singular and 
`NPS` for plural. 

### Pronouns

Most pronouns are grouped under `PP`, including 
when inflected for nominative or accusative case 
and reflexive pronouns. Possessive pronouns
(genitive case) are grouped under `PP$`. 

### Verbs

The base form of verbs (lexeme entry) is tagged 
as `VB`. This includes imperaties, infinitives, 
and subjunctives. 

Past tense verbs are tagged with `VBD`. Gerunds/
present participles are tagged with `VBG`. Past 
participles are tagged with `VBN`. 

Present tense verbs are divided into 3rd person 
singular `VBZ` and everything else `VBP`. 

In the original Mad Libs, verbs are either the 
base form ("verb") or the gerund form ("verb 
ending with 'ing'"). 

### Improvements

Using these tags, I updated the text processor to 
include adjectives, adverbs, numbers, exclamations, 
singular/plural nouns and proper nouns, and verbs, 
both the base form and the gerund form. 
