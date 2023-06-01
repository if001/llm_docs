from db import get_k8s_db, get_langchain_db, similarity_search_by_score
from llm import get_embeddings, get_llm
from llm_lora import get_llm as get_llm_lora
from prompt import (
    create_first_prompt, 
    create_add_info_react_prompt, 
    create_qa_prompt,
    create_doc_prompt
)
from utils import get_tool, get_final_answer
from langchain.agents.react.base import DocstoreExplorer
from langchain.tools import DuckDuckGoSearchRun

llm = get_llm_lora()
qa = "podについて教えてください"
prompt = create_first_prompt(qa)
r = llm(prompt)
print(r)
exit(0)

embd = get_embeddings()
k8s_doc = get_k8s_db(embd)

dd_search = DuckDuckGoSearchRun()

# llm = get_llm()
llm = get_llm_lora()


qa = "podについて教えてください"
docs = k8s_doc.similarity_search(qa, k=3)
doc_text = '\n'.join([v.page_content for v in docs])
doc_text = doc_text[:600]
print('doc_text', doc_text)
prompt = create_doc_prompt(qa, doc_text)
r = llm(prompt)
print('r:', r)

exit(0)


while True:
    while True:
        prompt = create_first_prompt(qa)
        output = llm(prompt)
        print('first result: ', output)
        print("="*100)
        output = output + '\n'

        action, action_input = get_tool(output)

        print('action:', action)
        print('actoin_input:', action_input)
        print("="*100)        
        if action and action_input:
            break

    tool_result = None
    if action == 'Web検索':
        tool_result = dd_search.run(action_input.strip())
        tool_result.strip()
    elif action == 'kubernetesのdocument検索':
        docs = k8s_doc.similarity_search(action_input.strip(), k = 1)
        tool_result = docs[0].page_content
    else:
        tool_result = None

    if tool_result != None and tool_result != '':
        tool_result = tool_result[:250]
        print('tool_result', tool_result)        
        print("-"*100)
        # tool_prompt = create_summary_prompt(tool_result[500:])
        # tool_result = llm(tool_prompt)
        # print('tool_result summary', tool_result)
        # print('--------------------')

        prompt = create_add_info_react_prompt(qa, tool_result)
        print('react prompt', prompt)
        print("-"*100)    
        output = llm(prompt)
        print('react result: ', output)        
        print("-"*100)
        output = output + '\n'        
        print("="*100)
        final_answer = get_final_answer(output)
        if final_answer:
            break
print('final:', final_answer)
print("-"*100)
qa_prompt = create_qa_prompt(qa, final_answer)
result = llm(qa_prompt)
print('result: ', result)
