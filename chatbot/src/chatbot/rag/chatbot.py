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
You are a RAG chatbot for Sonoma State University's academic catalog.
The context will either be a program or course from the catalog.   
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Offer access to an Outreach Counselor for more information at https://admissions.sonoma.edu/visit-ssu/meet-your-outreach-counselors.
Keep the answer as concise as possible.

When you use information from the context, you MUST cite the source using [Source X] notation, where X is the number of the source. 
The citations should appear at the end the reply.

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

    def add_source_footnotes_with_links(self, response: str) -> str:
        """Add a footnotes section with HTML links at the end of the response."""
        # First, check if we have documents to reference
        if not hasattr(self, 'latest_docs') or not self.latest_docs:
            return response

        # Create the footnotes section
        footnotes_section = "\n\n<hr>\n<h3>Sources:</h3>\n<ol>"

        # Keep track of which sources are actually cited in the response
        cited_sources = set()

        # Find all [Source X] citations in the response
        source_pattern = r'\[Source (\d+)\]'
        for match in re.finditer(source_pattern, response):
            source_num = int(match.group(1))
            cited_sources.add(source_num)

        # Add an entry for each cited source
        for source_num in sorted(cited_sources):
            if 1 <= source_num <= len(self.latest_docs):
                doc = self.latest_docs[source_num - 1]
                doc_title = doc.metadata.get('source', 'Unknown Source')
                url = doc.metadata.get('url', None)

                if url:
                    footnotes_section += f'\n  <li id="source-{source_num}">{doc_title} - <a href="{url}" target="_blank">Link</a></li>'
                else:
                    footnotes_section += f'\n  <li id="source-{source_num}">{doc_title}</li>'

        footnotes_section += "\n</ol>"

        # Update all [Source X] references to be HTML links to the footnotes
        def replace_with_footnote_link(match):
            source_num = int(match.group(1))
            if source_num in cited_sources:
                return f'<a href="#source-{source_num}">[Source {source_num}]</a>'
            return match.group(0)

        linked_response = re.sub(source_pattern, replace_with_footnote_link,
                                 response)

        # Only add the footnotes section if there are cited sources
        if cited_sources:
            final_response = linked_response + footnotes_section
        else:
            final_response = linked_response

        return final_response

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