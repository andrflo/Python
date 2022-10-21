from pagerank import transition_model
from pagerank import crawl


def test_transition_model():
    corpus = crawl("corpus1")
    assert transition_model(corpus, "1.html", 0.85) == {"1.html": None, "2.html": None, "3.html": None}