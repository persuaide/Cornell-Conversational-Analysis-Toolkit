import urllib.request
import shutil
import os
import pkg_resources
import zipfile
import json

# returns a path to the dataset file
def download(name, verbose=True, data_dir=None, use_newest_version=True):
    """Use this to download (or use saved) convokit data by name.

    :param name: Which item to download. Currently supported:

        - "wiki-corpus": Wikipedia Talk Page Conversations Corpus (see
            http://www.cs.cornell.edu/~cristian/Echoes_of_power.html)
        - "supreme-corpus": Supreme Court Dialogs Corpus (see
            http://www.cs.cornell.edu/~cristian/Echoes_of_power.html)
        - "parliament-corpus": UK Parliament Question-Answer Corpus (see
            http://www.cs.cornell.edu/~cristian/Asking_too_much.html)
        - "conversations-gone-awry-corpus": Wiki Personal Attacks Corpus (see
            http://www.cs.cornell.edu/~cristian/Conversations_gone_awry.html)
    :param data_dir: Output path of downloaded file (default: ~/.convokit)
    :param use_newest_version: Redownload if new version is found

    :return: The path to the downloaded item.
    """
    top = "http://zissou.infosci.cornell.edu/socialkit/"

    reddit_base_dir = "http://zissou.infosci.cornell.edu/convokit/datasets/subreddit-corpus/"
    cur_version = {
        "supreme-corpus": 2,
        "wiki-corpus": 2,
        "parliament-corpus": 2,
        "tennis-corpus": 2,
        "reddit-corpus": 2,
        "reddit-corpus-small": 2,
        "conversations-gone-awry-corpus": 2,
        "movie-corpus": 1,
        "subreddit": 0,
    }

    DatasetURLs = {
        "supreme-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/supreme-corpus/full.corpus",
       
        "wiki-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/wiki-corpus/full.corpus",
       
        "parliament-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/parliament-corpus/full.corpus",

        "tennis-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/tennis-corpus/full.corpus",

        "movie-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/movie-corpus/full.corpus",

        # "reddit-corpus": top + \
        #     "datasets/reddit-corpus/full.json",

        # "reddit-corpus-small": top + \
        #     "datasets/reddit-corpus/small.json",

        "conversations-gone-awry-corpus": "http://zissou.infosci.cornell.edu/convokit/"
            "datasets/conversations-gone-awry-corpus/full.corpus",
        
        "reddit-corpus-small": reddit_base_dir + "reddit-corpus-small.corpus", 


        "parliament-motifs": [
            top + \
            "datasets/parliament-corpus/parliament-motifs/answer_arcs.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_arcs.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_fits.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_fits.json.super",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_supersets_arcset_to_super.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_supersets_sets.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_tree_arc_set_counts.tsv",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_tree_downlinks.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_tree_edges.json",
            top + \
            "datasets/parliament-corpus/parliament-motifs/question_tree_uplinks.json"

        ],
        "supreme-motifs": [
            top + \
            "datasets/supreme-corpus/supreme-motifs/answer_arcs.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_arcs.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_fits.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_fits.json.super",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_supersets_arcset_to_super.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_supersets_sets.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_tree_arc_set_counts.tsv",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_tree_downlinks.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_tree_edges.json",
            top + \
            "datasets/supreme-corpus/supreme-motifs/question_tree_uplinks.json"

        ],
        "tennis-motifs": [
            top + \
            "datasets/tennis-corpus/tennis-motifs/answer_arcs.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_arcs.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_fits.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_fits.json.super",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_supersets_arcset_to_super.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_supersets_sets.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_tree_arc_set_counts.tsv",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_tree_downlinks.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_tree_edges.json",
            top + \
            "datasets/tennis-corpus/tennis-motifs/question_tree_uplinks.json"

        ],
        "wiki-motifs": [
            top + \
            "datasets/wiki-corpus/wiki-motifs/answer_arcs.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_arcs.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_fits.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_fits.json.super",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_supersets_arcset_to_super.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_supersets_sets.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_tree_arc_set_counts.tsv",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_tree_downlinks.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_tree_edges.json",
            top + \
            "datasets/wiki-corpus/wiki-motifs/question_tree_uplinks.json"

        ]

    }
    
    if not name.startswith("subreddit"): 
        name = name.lower()
    else:
        subreddit_name = name.split("-")[1]
        print(subreddit_name)
        cur_version[name] = cur_version['subreddit']
        DatasetURLs[name] = get_subreddit_info(subreddit_name)
        print(DatasetURLs[name])

    if data_dir is None:
        data_dir = os.path.expanduser("~/.convokit/")
        #pkg_resources.resource_filename("convokit", "")
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    parent_dir = os.path.join(data_dir, "downloads")
    dataset_path = os.path.join(data_dir, "downloads", name)
    if not os.path.exists(os.path.dirname(dataset_path)):
        os.makedirs(os.path.dirname(dataset_path))


    downloadeds_path = os.path.join(data_dir, "downloads", "downloaded.txt")
    if not os.path.isfile(downloadeds_path):
        open(downloadeds_path, "w").close()
    with open(downloadeds_path, "r") as f:
        downloaded_lines = f.read().splitlines()
        downloaded = {}
        for l in downloaded_lines:
            dname, version = l.split(" ")
            version = int(version)
            if dname not in downloaded or downloaded[dname] < version:
                downloaded[dname] = version

    if name not in downloaded or \
        (use_newest_version and name in cur_version and
            downloaded[name] < cur_version[name]):

        if name.endswith("-motifs"):
            for url in DatasetURLs[name]:
                full_name = name + url[url.rfind('/'):]
                if full_name not in downloaded:
                    motif_file_path = dataset_path + url[url.rfind('/'):]
                    if not os.path.exists(os.path.dirname(motif_file_path)):
                        os.makedirs(os.path.dirname(motif_file_path))
                    download_helper(motif_file_path, url, verbose, full_name, downloadeds_path)
        else:
            url = DatasetURLs[name]
            download_helper(dataset_path, url, verbose, name, downloadeds_path)
    parent_dir = os.path.join(parent_dir, name)
    return parent_dir

def download_helper(dataset_path, url, verbose, name, downloadeds_path):
    
    if url.lower().endswith(".corpus") or url.lower().endswith(".corpus.zip"):
        dataset_path += ".zip"

    with urllib.request.urlopen(url) as response, \
            open(dataset_path, "wb") as out_file:
        if verbose:
            l = float(response.info()["Content-Length"])
            length = str(round(l / 1e6, 1)) + "MB" \
                if l > 1e6 else \
                str(round(l / 1e3, 1)) + "KB"
            print("Downloading", name, "from", url,
                  "(" + length + ")...", end=" ", flush=True)
        shutil.copyfileobj(response, out_file)

    # post-process (extract) corpora
    if name.startswith("subreddit"):
        with zipfile.ZipFile(dataset_path, "r") as zipf:
            corpus_dir = os.path.join(os.path.dirname(downloadeds_path), name)
            if not os.path.exists(corpus_dir):
                os.mkdir(corpus_dir)
            zipf.extractall(corpus_dir)
    
    elif url.lower().endswith(".corpus"):
        #print(dataset_path)
        with zipfile.ZipFile(dataset_path, "r") as zipf:
            zipf.extractall(os.path.dirname(downloadeds_path))

    if verbose:
        print("Done")
    with open(downloadeds_path, "a") as f:
        fn = os.path.join(os.path.dirname(downloadeds_path), name)
        f.write("{} {}\n".format(name, corpus_version(fn)))
        #f.write(name + "\n")

def corpus_version(filename):
    with open(os.path.join(filename, "index.json")) as f:
        d = json.load(f)
        return int(d["version"])

# retrieve grouping and completes the download link for subreddit
def get_subreddit_info(subreddit_name):

    # base directory of subreddit corpuses
    subreddit_base = "http://zissou.infosci.cornell.edu/convokit/datasets/subreddit-corpus/"
    data_dir = os.path.join(subreddit_base, "corpus-zipped")
    
    groupings_url = subreddit_base + "subreddit-groupings.txt"
    groups_fetched = urllib.request.urlopen(groupings_url) 
    
    groups = [line.decode("utf-8").strip("\n") for line in groups_fetched]

    for group in groups:
        if subreddit_in_grouping(subreddit_name, group):
            return os.path.join(data_dir, group, subreddit_name + ".corpus.zip")

    print("The subreddit requested is not available.")

    return ""

def subreddit_in_grouping(subreddit: str, grouping_key: str):
    """
    :param subreddit: subreddit name
    :param grouping_key: example: "askreddit~-~blackburn"
    :return: if string is within the grouping range
    """
    bounds = grouping_key.split("~-~")
    if len(bounds) == 1:
        print(subreddit, grouping_key)
    return bounds[0] <= subreddit <= bounds[1]


def meta_index(corpus=None, filename=None):
    keys = ["utterances-index", "conversations-index", "users-index",
            "overall-index"]
    if corpus is not None:
        return {k: v for k, v in corpus.meta_index.items() if k in keys}
    if filename is not None:
        with open(os.path.join(filename, "index.json")) as f:
            d = json.load(f)
            return d