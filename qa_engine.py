from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def answer_query(query, index):
    similar_docs = index.similarity_search(query, k=3)
    llm = ChatOpenAI(temperature=0)
    chain = load_qa_chain(llm, chain_type="stuff")

    answer = chain.run(input_documents=similar_docs, question=query)
    sources = [doc.metadata.get('source', 'N/A') for doc in similar_docs]
    return answer, sources
