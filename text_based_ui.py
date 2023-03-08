# Lauryn Anderson
# MIT License

import pandas

from text_processing import preprocess_text


def main():
    while True:
        text = input('Enter text to blankit:\n')
        tokens = preprocess_text(text)
        if not tokens.empty:
            output = fill_blanks(tokens)
            print('Here is your complete blankit:\n' + output)

        repeat = input('Enter "y" to play again:\n')
        if repeat != "y":
            break


def fill_blanks(tokens):
    output = ''
    print('Please input the following parts of speech:')
    for _, token in tokens.iterrows():
        if pandas.isnull(token['prompt']):
            output += token['token'].text
        else:
            output += input(token['prompt'] + '\n')
        output += token['token'].whitespace_

    return output


main()
