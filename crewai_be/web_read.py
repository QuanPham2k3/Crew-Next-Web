from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()


def get_vectorstore_from_url(url):
    """
    Function loads a document from a URL and converts it into a vector store.

    Parameters:url (str): The URL of the document to load.

    Returns:vector_store: The vector store created from the document.
    """
    loader = WebBaseLoader(url)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

    return vector_store


def get_context_retriever_chain(vector_store):
    """
    Function creates a context retriever chain from a vector store.

    Parameters:vector_store: The vector store to create the context retriever chain from.

    Returns:retriever_chain: The created context retriever chain.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")  # Replace with actual model if available

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
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")  # Replace if needed

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

# def get_response(user_input):
#     retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
#     conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
#     response = conversation_rag_chain.invoke({
#         "chat_history": st.session_state.chat_history,
#         "input": user_input
#     })
    
#     return response['answer']

# # app config
# st.set_page_config(page_title="Chat with websites", page_icon="🤖")
# st.title("Chat with websites")

# # sidebar
# with st.sidebar:
#     st.header("Settings")
#     website_url = st.text_input("Website URL")

# if website_url is None or website_url == "":
#     st.info("Please enter a website URL")

# else:
#     # session state
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = [
#             AIMessage(content="Hello, I am a bot. How can I help you?"),
#         ]
#     if "vector_store" not in st.session_state:
#         st.session_state.vector_store = get_vectorstore_from_url(website_url)    

#     # user input
#     user_query = st.chat_input("Type your message here...")
#     if user_query is not None and user_query != "":
#         response = get_response(user_query)
#         st.session_state.chat_history.append(HumanMessage(content=user_query))
#         st.session_state.chat_history.append(AIMessage(content=response))
        
       

#     # conversation
#     for message in st.session_state.chat_history:
#         if isinstance(message, AIMessage):
#             with st.chat_message("AI"):
#                 st.write(message.content)
#         elif isinstance(message, HumanMessage):
#             with st.chat_message("Human"):
#                 st.write(message.content)