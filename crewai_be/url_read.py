from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
#from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_groq import ChatGroq
load_dotenv()
LlmGrog = ChatGroq(model = 'llama3-70b-8192') #llama3-8b-8192

def get_vectorstore_from_url(url):
    """
    Function loads a document from a URL and converts it into a vector store.
    Parameters:url (str): The URL of the document to load.
    Returns:vector_store: The vector store created from the document.
    """
    loader = WebBaseLoader(url)
    document = loader.aload()

    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    vector_store = Chroma.from_documents(document_chunks, GPT4AllEmbeddings()) #OpenAIEmbeddings() 

    return vector_store


def get_context_retriever_chain(vector_store):
    """
    Function creates a context retriever chain from a vector store.
    Parameters:vector_store: The vector store to create the context retriever chain from.
    Returns:retriever_chain: The created context retriever chain.
    """
    llm = LlmGrog
    # ChatOpenAI(model="gpt-3.5-turbo-0125")  # Replace with actual model if available

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation.")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain


def get_conversational_rag_chain(retriever_chain):
    """
    Function creates a conversational RAG chain from a context retriever chain.
    Parameters:retriever_chain: The context retriever chain to create the conversational RAG chain from.
    Returns:retrieval_chain: The created conversational RAG chain.
    """
    llm = LlmGrog
    # ChatOpenAI(model="gpt-3.5-turbo-0125")  # Replace if needed

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


def get_response(user_input, vector_store):
    """
    Function generates a response to a user's input using a conversational RAG chain.
    Parameters:
        user_input (str): The user's input.
        vector_store: The vector store to use for creating the conversational RAG chain.
    Returns:response (str): The generated response.
    """
    retriever_chain = get_context_retriever_chain(vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": [],  # Assuming empty chat history for API calls
        "input": user_input
    })
    
    return response['answer']

# run test
def main():
    urls= [""]

    vector_store = get_vectorstore_from_url(urls)
    user_query = "summarize the document"
    answer = get_response(user_query, vector_store)
    print(answer)
if __name__ == '__main__':
    main()