from langchain import PromptTemplate
 
# This template tells the model exactly when/how to mention whether it used the context.
CUSTOM_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant. You have access to some retrieved document passages (below).  
Your job is twofold:
  1) If the answer can be found (verbatim or paraphrased) in the passages, respond with:
       "I used the provided documents to answer*: <your answer here>"
  2) If the passages do NOT contain any information that answers the question, respond with:
       "I did not find the answer in the provided documents. Answer from my own knowledge*: <your answer here>"
 
Passages:
{context}
 
Question: {question}
 
Answer exactly in one of the two formats above.
""".strip(),
)