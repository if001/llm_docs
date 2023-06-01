def get_embeddings():
    from langchain.embeddings import LlamaCppEmbeddings

    model_path='../llama.cpp/models/ggml-vic13b-q5_1.bin'
    model_path='../llama.cpp/models/ggml-wizardlm-7b-q8_0.bin'

    embeddings = LlamaCppEmbeddings(
        model_path=model_path,
        n_ctx=1024
    )
    return embeddings




def get_llm():
    from langchain.llms import LlamaCpp
    # model_path="../llama.cpp/models/ggml-vicuna-13b-4bit.bin"
    
    model_path='../llama.cpp/models/ggml-wizardlm-7b-q8_0.bin'
    model_path='../llama.cpp/models/wizard-vicuna-13B.ggml.q8_0.bin'
    

    stop = [
        '\nUSER: ',
        '\n\tUSER: ',
    ]
    llm = LlamaCpp(
        model_path=model_path,
        n_ctx=1024,
        max_tokens=256,
        seed=1,
        stop=stop,
        f16_kv=True
    )
    return llm