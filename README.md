# blankit

blankit is a fill-in-the-blank game generator.

Powered by SpaCy, it takes any paragraph and 
turns it into a MadLibs-style game where players 
suggest arbitrary words to fill in the blanks, 
producing hilarious nonsense.

## History

Initially developed in high school in 2017-18, 
this concept was originally implemented in Swift 
using the Swift Natural Language format. That 
project was rewarded with a scholarship to attend 
the Apple Worldwide Developers' Conference 2018. 

This Python/SpaCy reimplementation is to fulfill 
the course project requirements in the UCalgary 
CPSC 599.27 Natural Language Processing course, 
taught by Dr. Katie Ovens in Winter 2023. 

Building on the naive implementation, it 
incorporates more powerful NLP tools and 
customizations to make more informed choices 
when selecting words to be replaced.

This project was presented at the Verbatium Colloquium
at the University of Calgary on 1 April 2023. 
Slides available [here](/slides.pdf).

## Usage

Developed in a virtual environment where SpaCy was 
installed using the following commands:

```commandline
pip install pandas
pip install spacy
python -m spacy download en_core_web_sm
pip install coreferee
python -m coreferee install en
```

## License

[MIT License](https://choosealicense.com/licenses/mit/)
copyright (c) 2023 Lauryn Anderson
