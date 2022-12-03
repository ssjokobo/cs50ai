import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from math import log
import string
import sys
import os

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
    documents = dict()

    for document in os.listdir(directory):
        if document.endswith(".txt"):
            with open(os.path.join(directory, document)) as f:
                documents[document] = f.read()

    return documents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punct = string.punctuation
    stopw = stopwords.words("english")

    return [word for word in word_tokenize(document.lower()) if word not in punct and word not in stopw]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    total_docs = len(documents)

    for document in documents:
        for word in documents[document]:
            if word not in idfs:

                # Number of documents contaning the word
                num_docs_contain = 1
                for doc in documents:
                    if doc != document and word in documents[doc]:
                        num_docs_contain += 1
                idfs[word] = log(total_docs/num_docs_contain)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = {file: 0 for file in files}

    for word in query:
        for file in files:
            try:
                tf_idf = files[file].count(word) * idfs[word]
            except KeyError:
                tf_idf = 0
            file_scores[file] += tf_idf

    return [file[0] for file in sorted(file_scores.items(), key=lambda x:x[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = dict()

    for sentence in sentences:
        words_in_sentence = sentences[sentence]
        idf = 0
        density = 0
        for q_word in query:
            if q_word in words_in_sentence:
                idf += idfs[q_word]
                density += words_in_sentence.count(q_word)

        if idf > 0:
            sentence_scores[sentence] = (idf, density/len(words_in_sentence))

    return [sentence[0] for sentence in sorted(sentence_scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)][:n]


if __name__ == "__main__":
    main()
