import os
from google import genai
from google.genai import types

class GeminiEmbedder:
    def __init__(self, model="gemini-embedding-001", dimensions=768):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model = model
        self.dimensions = dimensions

    def fit(self, documents):
        pass  

    def embed_documents(self, texts):
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.dimensions,
            ),
        )
        return [embedding.values for embedding in response.embeddings]

    def embed_query(self, text):
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self.dimensions,
            ),
        )
        return response.embeddings[0].values

    