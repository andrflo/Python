from pagerank import transition_model
from pagerank import crawl


def test_transition_model():
    corpus = crawl("corpus1")
    assert transition_model()