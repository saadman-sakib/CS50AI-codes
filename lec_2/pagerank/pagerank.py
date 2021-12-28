import os
import random
import re
import sys

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

    transition_model_dict = dict()

    corpus_length = len(corpus)

    for _page in corpus:
        transition_model_dict[_page] = (1-DAMPING)/corpus_length

    page_no_in_page = len(corpus[page])

    for _page in corpus[page]:
        transition_model_dict[_page] += DAMPING/page_no_in_page

    return transition_model_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    from collections import Counter

    def next_page_generate(page):
        weights = []
        next_probable_pages = []

        page_transition_dict = transition_model(corpus, page, damping_factor)

        for page in page_transition_dict:
            weights.append(page_transition_dict[page])
            next_probable_pages.append(page)
        
        return random.choices(next_probable_pages, weights = weights, k=1)[0]

    this_page = random.choice(list(corpus.keys()))
    samples = []

    for i in range(n):
        next_page = next_page_generate(this_page)
        samples.append(next_page)
        this_page = next_page

    sample_count = Counter(samples)
    sum_of_sample_values = sum(list(sample_count.values()))

    for key in sample_count:
        sample_count[key] = sample_count[key] / sum_of_sample_values

    return sample_count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #page rank dictionary
    page_rank_dict = dict()

    N = len(corpus)

    #setting the probability of each page : 1/N
    for page in corpus:
        page_rank_dict[page] = 1/N

    #function of iteration
    def page_rank(page):
        rank_sum = 0
        for _page in corpus:
            if page in corpus[_page]:
                rank_sum += page_rank_dict[_page]/len(corpus[_page])

        return (1-damping_factor)/N + damping_factor*rank_sum

    flag = True
    while flag:
        flag = False
        for page in corpus:
            PR = page_rank(page)
            if (PR - page_rank_dict[page]) > .001 or (page_rank_dict[page] - PR) > .001:
                page_rank_dict[page] = PR
                flag = True
            else:
                page_rank_dict[page] = round(page_rank_dict[page] ,4)


    #normalizing again:
    value_sum = sum(list(page_rank_dict.values()))
    for page in page_rank_dict:
        page_rank_dict[page] = page_rank_dict[page] / value_sum



    return page_rank_dict


if __name__ == "__main__":
    main()
