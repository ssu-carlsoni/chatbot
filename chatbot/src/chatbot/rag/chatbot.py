from langchain.chains.conversational_retrieval.base import \
    ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI


class Chatbot:
    def __init__(self, knowledge_manager):
        self.knowledge_manager = knowledge_manager
    #     self.memory = ConversationBufferMemory(
    #         memory_key="chat_history",
    #         return_messages=True
    #     )
    #     self.chain = ConversationalRetrievalChain.from_llm(
    #         llm=ChatOpenAI(temperature=0.7),
    #         retriever=self.knowledge_manager.retriever,
    #         memory=self.memory,
    #     )
    #
    # async def get_response(self, message: str) -> str:
    #     response = self.chain({"question": message})
    #     return response['answer']

    def test(self):
        return self.knowledge_manager.retrieve("Math Courses")

