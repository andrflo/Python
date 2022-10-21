from pagerank import transition_model
from pagerank import crawl


def test_transition_model():
    corpus = crawl("corpus0")    
    assert transition_model(corpus, "1.html", 0.85) == {"1.html": 0.8875, "2.html": 0.4625, "3.html": 0.4625, "4.html": 0.8875}