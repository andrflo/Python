import os
import random
import re
import sys
from tkinter import N

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    tm = dict.fromkeys(corpus)    
    for p in tm:
        if (len(corpus[page]) == 0):
            tm[p] = 1/len(tm)
        else:    
            tm[p] = (1 - damping_factor)/len(tm)
            # If p can be reached from page
            if (p in corpus[page]):
                tm[p] += damping_factor * 1/(len(corpus[page]))
            tm[p] = round(float(tm[p]), 4)    
    return tm   


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_pr = dict.fromkeys(corpus)   
    for pr in sample_pr:
        sample_pr[pr] = 0
    #initial_page = (list(sample_pr))[random.randint(0, len(sample_pr)-1)]    
    initial_page = random.choice(list(sample_pr))  
    sample_pr[initial_page] = 1/n
    counter = n-1
    while counter>0:
        tm = transition_model(corpus, initial_page, damping_factor)
        initial_page = random.choices(list(sample_pr), weights=list(tm.values()), k=1)[0]  
        #print(initial_page)      
        sample_pr[initial_page] += 1/n
        counter -= 1
    for pr in sample_pr:
        sample_pr[pr] = round(float(sample_pr[pr]), 4)    
    return sample_pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterate_pr = dict.fromkeys(corpus) 
    
    n_pages = len(iterate_pr)
    constant = (1-damping_factor)/n_pages
    
    for pr in iterate_pr:
        iterate_pr[pr] = [1/n_pages]

    for pr in iterate_pr:        
        sum = 0
        for p in corpus:
            if pr in p:
                sum += iterate_pr[p]/len(corpus[p])
        iterate_pr[pr] =  constant + damping_factor*sum

    return iterate_pr


if __name__ == "__main__":
    main()
