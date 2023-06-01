import os 



def new_vector_db_from_sitemap(url, db_name, embeddings):
    from langchain.document_loaders.sitemap import SitemapLoader

    filter = 'https://kubernetes.io/ja/docs/tutorials/kubernetes-basics/'
    filter = 'https://kubernetes.io/ja/docs/tutorials/kubernetes-basics/deploy-app/'
    filter = 'https://kubernetes.io/ja/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/'
    # filter = "https://kubernetes.io/ja/docs/"
    
    loader = SitemapLoader(
        url,
        filter_urls=[filter]
    )
    docs = loader.load()

    print('start split')
    from langchain.text_splitter import RecursiveCharacterTextSplitter    
    text_splitter = RecursiveCharacterTextSplitter(
        ["\n", "。", ".", "\n\n", ""],
        chunk_size=500, 
        chunk_overlap=20,
        )
    texts = text_splitter.split_documents(docs)

    # for v in texts:
    #     print('text: ', v)
    #     print('-'*100)
        
    from langchain.vectorstores import Chroma

    print('create doc')
    docsearch = Chroma.from_documents(texts, embeddings, persist_directory=db_name)
    return docsearch

def new_vectore_db_from_git(clone_url, db_name, embeddings):
    from langchain.document_loaders import GitLoader
    def filter(file_path):
        # return "docs" in file_path and file_path.endswith(".md")
        return 'reference' in file_path and "docs" in file_path and file_path.endswith(".md")

    repo_dir_name = clone_url.split("/")[-1]
    base_dir = "./git_tmp/"
    repo_path = f"{base_dir}{repo_dir_name}"

    if os.path.exists(repo_path):
        loader = GitLoader(    
            repo_path=repo_path,
            branch="master",
            file_filter=filter
        )
    else:
        loader = GitLoader(
            clone_url=clone_url,
            repo_path=repo_path,            
            branch="master",
            file_filter=filter
        )    
    docs = loader.load()

    from langchain.text_splitter import CharacterTextSplitter
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    from langchain.text_splitter import CharacterTextSplitter
    from langchain.vectorstores import Chroma

    
    docsearch = Chroma.from_documents(texts, embeddings, persist_directory=db_name)
    return docsearch

def load_db(db_name, embeddings):
    from langchain.vectorstores import Chroma
    docsearch = Chroma(embedding_function=embeddings, 
                   persist_directory=db_name)
    return docsearch


def get_langchain_db(embd):
    ## lanchain
    url = "https://github.com/hwchase17/langchain"
    db_name ='./chroma_persist/langchain'
    if os.path.exists(db_name):
        doc = load_db(db_name, embd)
    else:
        doc = new_vectore_db_from_git(url, db_name, embd)    
    return doc

def get_k8s_db(embd):
    ## k8s
    url = "https://kubernetes.io/sitemap.xml"
    db_name ='./chroma_persist/k8s'
    if os.path.exists(db_name):
        print(f'load...{db_name}')
        doc = load_db(db_name, embd)
    else:
        doc = new_vector_db_from_sitemap(url, db_name, embd)
    return doc


def similarity_search_by_score(db, query):
    docs = db.similarity_search_with_score(query, k=4)
    _score = 0
    _doc = None
    for doc, score in docs:
        if _score < score:
            _doc = doc
    return _doc