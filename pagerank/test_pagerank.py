from pagerank import transition_model
from pagerank import crawl


def test_transition_model():
    corpus = crawl("corpus0")
    #assert transition_model(corpus, "1.html", 0.85) == {'4.html': None, '3.html': None, '2.html': None, '1.html': None}
    assert transition_model(corpus, "1.html", 0.85) == {"1.html": None, "2.html": None, "3.html": None, "4.html": None}