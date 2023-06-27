from nltk import regexp_tokenize
import random


# TODO: write tests and doc

# tokenizes the input text
def get_corpus(filename):
    with open(filename, "r", encoding="utf-8") as f:
        my_text = f.read()
    tokens = regexp_tokenize(my_text, "[\S]+")
    return tokens


# makes simple Markov chain model
def get_chain(tokens):
    chain = {}
    for i in range(len(tokens) - 1):
        chain.setdefault(tokens[i], {})
        chain[tokens[i]].setdefault(tokens[i + 1], 0)
        chain[tokens[i]][tokens[i + 1]] += 1
    return chain


# shows possible tails of the input head and their counts
def show_tails(chain_model):
    while True:
        user_input = input().strip()
        if user_input == 'exit':
            return
        else:
            valid = user_input in list(chain_model.keys())
            if valid:
                tails_freq = chain_model[user_input]
                print(f'Head: {user_input}')
                for tail, count in tails_freq.items():
                    print(f'Tail: {tail}  Count: {count}')
            else:
                print('Key Error. The requested word is not in the model. Please input another word')


# generates simple random text with 10 tokens
def gen_random_text(chain_model):
    n = 10  # 10 tokens in sentence
    sent = [random.choice(list(chain_model.keys()))]
    for i in range(1, n):
        possible_words = list(chain_model[sent[i - 1]].keys())
        counts = list(chain_model[sent[i - 1]].values())
        next_word = random.choices(possible_words, counts)
        sent.append(next_word[0])
    print(' '.join(sent))


# checks if token is valid for a start of a sentence
def is_valid_start(word: str):
    return word.istitle() and word[-1] not in ['.', '!', '?']


# generates sentence with minimum 5 tokens that ends with correct punctuation
def gen_full_sentence(chain_model):
    min_n = 5  # minimum 5 tokens
    start_tokens = [word for word in list(chain_model.keys()) if is_valid_start(word)]
    sent = [random.choice(start_tokens)]
    while len(sent) < min_n or sent[-1][-1] not in ['.', '!', '?']:
        possible_words = list(chain_model[sent[-1]].keys())
        counts = list(chain_model[sent[-1]].values())
        next_word = random.choices(possible_words, counts)
        sent.append(next_word[0])
    print(' '.join(sent))


def main():
    filename = input().strip()  # 'corpus.txt'
    tokenized_corpus = get_corpus(filename)
    chain_model = get_chain(tokenized_corpus)
    # generate 10 sentences
    _ = [gen_full_sentence(chain_model) for _ in range(10)]


if __name__ == '__main__':
    main()
