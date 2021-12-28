import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dict = dict()
    for file in os.listdir(directory):
       with open(os.path.join(directory, file)) as f:
           file_dict[file] = f.read()
    
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    def condition(word):
        if word in nltk.corpus.stopwords.words("english"):
            return False
        for x in word:
            if x.isalpha() or x.isdigit():
                return True
        return False

    word_list = nltk.word_tokenize(document)
    word_list = list(filter(condition, word_list))
    new_word_list = []

    for word in word_list:
        new_word_list.append(word.lower())

    return new_word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words = set()
    total_doc = len(documents)

    for key, value in documents.items():
        words = words.union(set(value))

    for word in words:
        occurance = 0
        for key, value in documents.items():
            if word in value:
                occurance += 1
        idfs[word] = math.log(total_doc / occurance)

    return idfs



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranked_files = dict()

    def sum_of_tf_idfs(words):
        result = 0

        for word in query:
            if word in idfs:
                tf = words.count(word)
                tf_idf = tf * idfs[word]
                result += tf_idf

        return result

    for key, value in files.items():
        ranked_files[key] = sum_of_tf_idfs(value)

    ranked_list = [key for key, value in 
        sorted(ranked_files.items(), key=lambda item: item[1], reverse = True)]

    return ranked_list[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranked_sentences = dict()

    def query_term_density(sentence):
        term_density = 0
        total_words = len(sentence)

        for word in query:
            if word in sentence:
                term_density += 1

        return term_density / total_words
        
    def sum_of_idfs(sentence):
        return sum([idfs[word] for word in sentence if (word in query)])

    for key, value in sentences.items():
        ranked_sentences[key] = (sum_of_idfs(value), query_term_density(value))

    ranked_list = [key for key, value in sorted(
                                ranked_sentences.items(),
                                key=lambda item: (
                                    item[1][0], 
                                    item[1][1]
                                    ),
                                reverse = True
                                )
                            ]

    return ranked_list[:n]


if __name__ == "__main__":
    main()
