import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

class ImpactService:
    def __init__(self, embedding_service=None):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.embedding_service = embedding_service

    def analyze_change_impact(self, repository_content, proposed_change):
        context_documents = []
        if self.embedding_service:
            # Retrieve relevant documents based on the proposed change
            context_documents = self.embedding_service.get_relevant_documents(proposed_change)
            retrieved_context = "\n\n".join([f"File: {doc.metadata.get("source", "Unknown")}\nContent:\n{doc.page_content}" for doc in context_documents])
        else:
            retrieved_context = repository_content # Fallback to full content if embedding service not provided

        prompt_template = """You are an experienced software architect AI assistant. Based on the following repository content and the proposed change, analyze the potential impact. First, consider the provided retrieved context which should be most relevant. If the retrieved context is insufficient, use the broader repository content. Provide a detailed report.

Retrieved Context (most relevant files/chunks):
{retrieved_context}

Broader Repository Content (for additional context if needed):
{repository_content}

Proposed Change: {proposed_change}

Generate a change impact analysis report in the following structured format:

### Risk Level
[Estimate the risk level: Low, Medium, High]

### Affected Files
[List specific file paths that are likely to be affected by this change, with brief reasoning]

### Affected Modules
[List specific modules or logical components that are likely to be affected, with brief reasoning]

### Reasoning
[Provide a detailed explanation of why these files/modules are affected and the potential consequences of the change]

### Suggested Implementation Order
[Suggest a logical order for implementing the change to minimize risk]

### Confidence Score
[Your confidence in this analysis: High, Medium, Low]
"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["retrieved_context", "repository_content", "proposed_change"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)

        # Truncate content if it's too long for the LLM context window
        max_length = 10000  # Approximate token limit for Gemini-pro, adjust as needed
        if len(repository_content) > max_length:
            repository_content = repository_content[:max_length] + "\n... (content truncated)"
        if len(retrieved_context) > max_length:
            retrieved_context = retrieved_context[:max_length] + "\n... (retrieved context truncated)"

        impact_analysis = chain.run(
            retrieved_context=retrieved_context,
            repository_content=repository_content,
            proposed_change=proposed_change
        )
        return impact_analysis
