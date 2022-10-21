from pagerank import transition_model
from pagerank import crawl


def test_transition_model_corpus0():
    corpus = crawl("corpus0")    
    assert transition_model(corpus, "1.html", 0.85) == {"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375}
    assert transition_model(corpus, "2.html", 0.85) == {"1.html": 0.4625, "2.html": 0.0375, "3.html": 0.4625, "4.html": 0.0375}
    assert transition_model(corpus, "3.html", 0.85) == {"1.html": 0.0375, "2.html": 0.4625, "3.html": 0.0375, "4.html": 0.4625}
    assert transition_model(corpus, "4.html", 0.85) == {"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375}


#def test_transition_model_corpus1():
 #   corpus = crawl("corpus1")    
  #  assert transition_model(corpus, "1.html", 0.85) == {"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375}    