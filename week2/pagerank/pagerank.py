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
    prob_dist = {}
    if len(corpus[page]) == 0:
        for link in corpus:
            prob_dist[link] = 1 / len(corpus)
    else:
        for link in corpus[page]:
            prob_dist[link] = damping_factor / len(corpus[page])
        for link in corpus:
            if link in prob_dist:
                prob_dist[link] += (1 - damping_factor) / len(corpus)
            else:
                prob_dist[link] = (1 - damping_factor) / len(corpus)

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page = ""
    prob_dist = {}
    i = n

    for link in corpus:
        prob_dist[link] = 0

    while True:
        if i == n:
            page = random.choice(list(corpus.keys()))
            prob_dist[page] += 1
            i -= 1
        elif i > 0:
            next_prob_dist = transition_model(corpus, page, damping_factor)
            page = random.choices(list(next_prob_dist.keys()), list(next_prob_dist.values()))[0]
            prob_dist[page] += 1
            i -= 1
        else:
            break

    for link in prob_dist:
        prob_dist[link] = prob_dist[link] / n


    return prob_dist


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prob_dist = {}
    for link in corpus:
        prob_dist[link] = 1 / len(corpus)

        # deal with page with no link
        if corpus[link] == set():
            for page in corpus:
                corpus[link].add(page)

    while True:
        new_prob_dist = {}
        for destination in corpus:
            sum = 0
            for departure in corpus:
                if destination in corpus[departure]:
                    sum += prob_dist[departure] / len(corpus[departure])
            new_value = (1 - damping_factor) / len(corpus) + damping_factor * sum
            new_prob_dist[destination] = new_value

        counter = 0
        for link in prob_dist:
            if abs(prob_dist[link] - new_prob_dist[link]) < 0.001:
                counter += 1

        if counter == len(corpus):
            break
        else:
            prob_dist = new_prob_dist

    return prob_dist


if __name__ == "__main__":
    main()
