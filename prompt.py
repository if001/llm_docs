prefix = """質問に対しstep by stepで考えてください。"""

tools_prompt = """以下のツールが利用できます:
Web検索: Webページを検索する
kubernetesのdocument検索: kubernetesのdocumentのページを検索する"""

tools = """[Web検索]、[kubernetesのdocument検索]"""

react_prompt = f"""以下のフォーマットで出力して下さい。
- 課題: 質問に対しあなたが解決すべき課題
- 解決策: ツールを利用し、課題を解決するアイディア
- ツール選択: {tools}のどちらかのツールを選択を選択してください。
- ツールへの入力: ツールに入力するキーワードのみを出力して下さい。"""

react_prompt_final_answer = f"""{react_prompt}
(以下は最終的な答えを導くことができれば出力して下さい。)
- 最終的な答え: 質問に対する最終的な答えを出力して下さい。"""


def create_first_prompt(qa):
    return f"""ユーザー: {prefix}<NL><NL>{tools_prompt}<NL>{react_prompt}<NL>質問: <NL>システム: """

def create_first_prompt2(qa):
    return f"""{prefix}

{tools_prompt}

{react_prompt}

USER: {qa}
ASSISTANT: """


def create_add_info_react_prompt(qa, info):
    return f"""{prefix}

追加情報: {info}

{tools_prompt}

{react_prompt_final_answer}

USER: {qa}
ASSISTANT: """


def create_qa_prompt(qa, info):
    return f"""関連情報を用いて、質問に答えてください。

関連情報: {info}

USER: {qa}
ASSISTANT: """


def create_doc_prompt(qa, doc_text):
    return f"""質問: {qa}
関連情報: {doc_text}

USER: 関連情報から質問に答えるために必要な情報を抽出し、結果のみを出力して下さい。
ASSISTANT: """

