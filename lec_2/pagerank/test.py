import pagerank

print(pagerank.transition_model(pagerank.crawl('corpus0'),'1.html',.85))

print(pagerank.sample_pagerank(pagerank.crawl('corpus0'),.85,10000))

print(pagerank.crawl('corpus0'))