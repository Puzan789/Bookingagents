from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import os 
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGroq(temperature=0, model_name="Gemma2-9b-It")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
filepath="docs/ndc.pdf"

#rag for our rag_node
class AnswerRAG:
    def __init__(self, pdf_path=filepath, llm=llm, embeddings=embeddings):
        """
        Initialize the RAG system with PDF path, LLM, and embeddings model
        """
        self.llm = llm
        self.embeddings = embeddings
        
        # Load and process documents
        self.documents = self._process_pdf(pdf_path)
        
        # Initialize retrievers
        self.vectorstore = FAISS.from_documents(self.documents, self.embeddings)
        self.retriever_vectordb = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        self.keyword_retriever = BM25Retriever.from_documents(self.documents)
        
        # Setup ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.retriever_vectordb, self.keyword_retriever],
            weights=[0.5, 0.5]
        )
        
        # Setup prompt and chains
        self.prompt = self._create_prompt()
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.retrieval_chain = create_retrieval_chain(
            self.ensemble_retriever,
            self.document_chain
        )

    def _process_pdf(self, pdf_path):
        """
        Process PDF file and split into chunks
        """
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20
        )
        return text_splitter.split_documents(docs)

    def _create_prompt(self):
        """
        Create the prompt template for the LLM
        """
        return ChatPromptTemplate.from_template(
            """ Answer the following question based only on the provided context.
                Think step by step before providing a detailed answer.
                Dont response like based on the provided context all just be that document and answer on that context.
                <context>
                {context}
                </context>
                Question: {input}
            """
        )

    def query(self, text):
        """
        Query the RAG system with a question
        """
        response = self.retrieval_chain.invoke({'input': text})
        return response['answer']

    def update_retriever_weights(self, vector_weight, keyword_weight):
        """
        Update the weights of the ensemble retriever
        """
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.retriever_vectordb, self.keyword_retriever],
            weights=[vector_weight, keyword_weight]
        )
        # Recreate the retrieval chain with new weights
        self.retrieval_chain = create_retrieval_chain(
            self.ensemble_retriever,
            self.document_chain
        )