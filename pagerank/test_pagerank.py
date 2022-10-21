from pagerank import transition_model
from pagerank import crawl
from pagerank import sample_pagerank


def test_transition_model_corpus0():
    corpus = crawl("corpus0")   
    ans = transition_model(corpus, "1.html", 0.85)
    assert ans == {"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375}
    acc = 0
    for k in ans:
        acc += ans[k]
    assert round(acc,0) == 1
    ans = transition_model(corpus, "2.html", 0.85)
    assert ans == {"1.html": 0.4625, "2.html": 0.0375, "3.html": 0.4625, "4.html": 0.0375}
    acc = 0
    for k in ans:
        acc += ans[k]
    assert round(acc,0) == 1
    ans = transition_model(corpus, "3.html", 0.85)
    assert ans == {"1.html": 0.0375, "2.html": 0.4625, "3.html": 0.0375, "4.html": 0.4625}
    acc = 0
    for k in ans:
        acc += ans[k]
    assert round(acc,0) == 1
    ans = transition_model(corpus, "4.html", 0.85)
    assert ans == {"1.html": 0.0375, "2.html": 0.8875, "3.html": 0.0375, "4.html": 0.0375}
    acc = 0
    for k in ans:
        acc += ans[k]
    assert round(acc,0) == 1

def test_transition_model_corpus1():
    corpus = crawl("corpus1")    
    ans = transition_model(corpus, "bfs.html", 0.85)
    assert ans == {"bfs.html": 0.0214, "dfs.html": 0.0214, "games.html": 0.0214, "minesweeper.html": 0.0214, "minimax.html": 0.0214, "search.html": 0.8714, "tictactoe.html": 0.0214}    
    acc = 0
    for k in ans:
        acc += ans[k]
    assert round(acc,0) == 1

def test_sample_pagerank(): 
    corpus = crawl("corpus0")   
    ans = sample_pagerank(corpus, 0.85, 1)  
    assert ans == {"1.html": None, "2.html": None, "3.html": None, "4.html": None}