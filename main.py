from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import MatchingEngine
from google.cloud import aiplatform
import time
from dotenv import load_dotenv
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


project_id="duet-ai-test-400118"
loader = PyPDFLoader("data/state-of-k8-cost-opt.pdf")

data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(data)

aiplatform.init(project=f"{project_id}")
embeddings = VertexAIEmbeddings()

texts = [
    "The cat sat on",
    "the mat.",
    "I like to",
    "eat pizza for",
    "dinner.",
    "The sun sets",
    "in the west.",
]

print(texts)
vector_store = MatchingEngine.from_components(
    texts=texts,
    project_id="duet-ai-test-400118",
    region="us-central1",
    gcs_bucket_uri="my-vector-store-bucket",
    index_id="<my_matching_engine_index_id>",
    endpoint_id="<my_matching_engine_endpoint_id>",
)

vector_store.add_texts(texts=texts)

vector_store.similarity_search("lunch", k=2)


query = "What is workload rightsizing"
docs = vectorstore.similarity_search(query)

# Here's an example of the first document that was returned
for doc in docs:
    print (f"{doc.page_content}\n")
