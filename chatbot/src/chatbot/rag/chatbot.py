from typing import AsyncGenerator
import re

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from chatbot.rag.knowledge_manager import KnowledgeManager


class Chatbot:
    def __init__(self, knowledge_manager: KnowledgeManager):
        self.knowledge_manager = knowledge_manager
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.rag_chain = self.get_rag_chain()
        self.latest_docs = []

    def get_rag_chain(self):
        template = """
You are a RAG Chatbot for Sonoma State University's academic catalog. Your purpose is to help users explore the catalog by providing information about programs and courses.

Use the provided context to answer questions, but do not speculate or provide information beyond the given sources. If the answer is unclear or uncertain, state that you don’t know and recommend speaking with an academic advisor. Keep responses neutral, professional, and concise. Avoid definitive statements about policies, requirements, or personal academic decisions—always encourage users to verify details with an advisor if necessary.

When using information from the context, you must cite the source inline using this format: [Source X] where X is the number of the source. If multiple sources apply, list them separately, e.g., [Source 1] [Source 2] [Source 4].

Do not generate opinions, personal advice, or interpretations. Do not respond to questions unrelated to the catalog. Do not generate any inappropriate, offensive, or misleading content.


The context will either be a program or course from the catalog.   
Use the following pieces of context to answer the question at the end.
If you don't know the answer, do not make one up, just say you don't know.
Keep the answer as concise as possible.

When you use information from the context, you MUST cite the source inline using the following format:
[Source X] where X is the number of the source.
Only include one source per citation bracket. If multiple sources apply, list them separately, e.g., [Source 1] [Source 2] [Source 4].

{context}

Question: {question}

Helpful Answer (with citations):
"""
        custom_rag_prompt = PromptTemplate.from_template(template)
        return (
                {
                    "context": lambda x: self.format_docs_with_sources(
                        x["docs"]),
                    "question": lambda x: x["question"]
                }
                | custom_rag_prompt
                | self.llm
                | StrOutputParser()
                | self.add_source_footnotes_with_links
        )

    def format_docs_with_sources(self, docs: list[Document]) -> str:
        """Format documents with source numbers for citation."""
        formatted_docs = []
        # Store the documents for later reference
        self.latest_docs = docs

        for i, doc in enumerate(docs, 1):
            doc_title = doc.metadata.get('source', 'Unknown Source')
            source_info = f"Source {i}: {doc_title}"
            formatted_content = f"{source_info}\n{doc.page_content}"
            formatted_docs.append(formatted_content)

        return "\n\n".join(formatted_docs)

    def add_source_footnotes_with_links(self, text: str) -> str:
        # get sources and positions
        sources = {}
        current_index = 1
        source_ids = re.findall(r'\[Source (\d+)\]', text)
        for source_id in source_ids:
            source_id = int(source_id)
            if source_id not in sources.values():
                sources[current_index] = source_id
                current_index += 1

        # replace sources with superscript based on position
        processed_text = text
        for index, source_id in sources.items():
            processed_text = processed_text.replace(
                f'[Source {source_id}]',
                f'<sup class="text-secondary">{index}</sup>'
            )

        processed_text += "\n<hr>\n"
        for index, source_id in sources.items():
            doc = self.latest_docs[source_id - 1]
            url = doc.metadata.get('source')
            title = doc.metadata.get('course_name')
            if not title:
                title = doc.metadata.get('program_name')
            processed_text += (f'<sup class="text-secondary">{index}</sup><a href="{url}"'
                               f'>{title}</a><br>\n')
            index += 1

        # processed_text = text + "\n<br>---</br>\n" + processed_text
        return processed_text

    async def get_response(self, message: str) -> str:
        docs = self.knowledge_manager.retrieve(message)
        self.latest_docs = docs
        response = await self.rag_chain.ainvoke({
            "docs": docs,
            "question": message
        })
        return response

    async def get_streaming_response(self, message: str) -> AsyncGenerator[
        str, None]:
        docs = self.knowledge_manager.retrieve(message)
        self.latest_docs = docs

        # For streaming, we'll collect the full response and process it at the end
        complete_response = ""

        async for chunk in self.rag_chain.astream({
            "docs": docs,
            "question": message
        }):
            complete_response += chunk
            yield chunk

        # After streaming is complete, we can process the full response
        # Note: This won't affect what was already streamed, but could be used
        # if you need the processed result elsewhere
        processed_response = self.add_source_footnotes_with_links(
            complete_response)