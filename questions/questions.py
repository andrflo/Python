import nltk
import sys
import os
import string
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
    path_proj = os.path.abspath(os.getcwd())
    filenames = os.listdir(directory)
    dictfiles = {x: "" for x in filenames}
    for filename in filenames:
        with open(os.path.join(path_proj, directory, filename)) as file:
            dictfiles[filename] = file.read()
    
    return dictfiles        


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    listwords = [x.lower() for x in nltk.tokenize.word_tokenize(document)]
    listfilteredwords = []
    for w in listwords:
        if not (w in string.punctuation or w in nltk.corpus.stopwords.words("english")):
            listfilteredwords.append(w)          
    return listfilteredwords        


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    numberDocs = len(documents)
    listwords = []
    for doc in documents:
        listwords.extend(documents[doc])
    setwords = set(listwords) 

    dictRes = {x: 0 for x in setwords}
    for word in dictRes:
        for doc in documents:
            if word in documents[doc]:
                dictRes[word] += 1
    for word in dictRes:
        dictRes[word] = math.log(numberDocs/dictRes[word])    
    return dictRes


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """    
    listrankfiles = [[x, 0] for x in files]
    
    for word in query:
        idf = idfs[word]
        for el in listrankfiles:
            c = files[el[0]].count(word)
            el[1] += c*idf 

    listrankfiles.sort(key=lambda t: t[1], reverse = True)

    #print(listrankfiles[0:n])    
    return [x[0] for x in listrankfiles[0:n]]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    listranksen = [[x, 0, 0] for x in sentences]

    for word in query:
        idf = idfs[word]
        for el in listranksen: 
            if word in sentences[el[0]]:           
                el[1] += idf 
                el[2] += 1

    listranksen.sort(key=lambda t: ( t[1], t[2]/len(tokenize(t[0])) ), reverse = True)            

    #print(listranksen[0:n])    
    return [x[0] for x in listranksen[0:n]]


if __name__ == "__main__":
    main()
