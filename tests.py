# Lauryn Anderson

from text_processing import preprocess_text
import pandas

# WIRED. 2023. What Will Ethical Space Exploration Look Like? Retrieved March 7, 2023 from
# https://www.wired.com/story/erika-nesvold-what-will-ethical-space-exploration-look-like/

newspaper_sample = """
IF THE DREAMS of space agencies and private companies come to fruition, 
within a couple of decades we’ll have orbiting hotels and lunar mining 
colonies, and the first human visitors will be en route to the Red Planet. 
But astrophysicist Erika Nesvold argues that the shape of tomorrow’s space 
expeditions and conflicts could depend on ethical choices people make 
today. Nesvold is coeditor of the book Reclaiming Space, which was 
published today, and the author of Off-Earth, due out on March 7. She’s 
also a cofounder of JustSpace Alliance, a nonprofit organization that 
advocates for a more inclusive and ethical future in space, and a developer 
for Universe Sandbox, a physics-based space simulator.
"""

interview_sample = """
WIRED: What first drew you to study the ethics of space exploration?

Erika Nesvold: I’m an astrophysicist by training, and I was out in 
Silicon Valley doing a really fun six-week NASA program about planetary 
defense. As part of that, I got to meet a lot of people working in the 
private space industry. That was a great experience, but I found I was very 
disappointed with some of the answers they gave to my questions.
"""

# J. Kenji Lopez-Alt. 2023. Easy All-Purpose Barbecue Sauce. Serious Eats. Retrieved March
# 7, 2023 from https://www.seriouseats.com/easy-basic-barbecue-rub-sauce-all-purpose-recipe

recipe_sample = """
Easy All-Purpose Barbecue Sauce

This versatile sauce combo is perfect on a wide variety of barbecued and 
grilled foods, like ribs, chicken, or burgers.

Ingredients

1 cup (240ml) chicken broth
1/2 cup (120ml) ketchup
1/4 cup (60ml) dark molasses, plus more to taste
1 small onion, grated on the large holes of a box grater (about 4 ounces)
2 tablespoons (30ml) Worcestershire sauce
1 tablespoon (15ml) brown mustard
2 tablespoons (30ml) cider vinegar, plus more to taste
2 teaspoons (10ml) hot sauce, plus more to taste
2 tablespoons (25g) spice rub
1 teaspoon (5ml) liquid smoke, such as Wright's (optional)

Directions

Combine all sauce ingredients in a small saucepan over medium-low heat. 
Whisk together and simmer until reduced to a glaze consistency, about 15 
minutes (sauce should reduce by about one-third). Adjust flavor with more 
molasses, vinegar, or hot sauce to taste. Cooled barbecue sauce can be 
stored in a sealed container in the refrigerator for several months.
"""

# Jane Austen. 1813. Pride and Prejudice. Public Domain. Retrieved March 7, 2023 from
# https://gutenberg.org/ebooks/1342

literature_sample = """
It is a truth universally acknowledged, that a single man in possession of 
a good fortune must be in want of a wife.

However little known the feelings or views of such a man may be on his first 
entering a neighbourhood, this truth is so well fixed in the minds of the 
surrounding families, that he is considered as the rightful property of some 
one or other of their daughters.

"My dear Mr. Bennet," said his lady to him one day, "have you heard that 
Netherfield Park is let at last?"

Mr. Bennet replied that he had not.

"But it is," returned she; "for Mrs. Long has just been here, and she told me 
all about it."

Mr. Bennet made no answer.
"""

# Paul Simon. 1975. 50 Ways To Leave Your Lover. Retrieved March 7, 2023 from
# https://genius.com/Simon-and-garfunkel-50-ways-to-leave-your-lover-lyrics

lyrics_sample = """
"The problem is all inside your head," she said to me
"The answer is easy if you take it logically
I'd like to help you in your struggle to be free
There must be 50 ways to leave your lover."

She said, "It's really not my habit to intrude
Furthermore, I hope my meaning won't be lost or misconstrued
But I'll repeat myself at the risk of being crude
There must be 50 ways to leave your lover."
50 ways to leave your lover

You just slip out the back, Jack
Make a new plan, Stan
You don't need to be coy, Roy
Just get yourself free

Hop on the bus, Gus
You don't need to discuss much
Just drop off the key, Lee
And get yourself free
"""

samples = [
    newspaper_sample, interview_sample, recipe_sample, literature_sample, lyrics_sample
]


def test():
    for text in samples:
        tokens = preprocess_text(text)
        if not tokens.empty:
            output = fill_blanks(tokens)
            print(output + '\n\n')


def fill_blanks(tokens):
    output = ''
    for _, token in tokens.iterrows():
        if pandas.isnull(token['prompt']):
            output += token['token'].text
        else:
            output += token['prompt']
        output += token['token'].whitespace_

    return output


test()
