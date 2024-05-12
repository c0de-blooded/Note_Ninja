from getTextPDF import *
from topics_excavator import *
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
import torch
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Read the document from PDF
doc = pdf_reader("./uploads/file.pdf")

load_dotenv(Path(".env"))
def getsentences(text, topic):
    # Chunk the document into smaller parts (adjust max_chunk_length as needed)
    max_chunk_length = 512
    doc_chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]

    # Load SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Calculate embeddings for each chunk
    chunk_embeddings = model.encode(doc_chunks, convert_to_tensor=True)

    # Calculate embeddings for the topic
    topic_embedding = model.encode([topic], convert_to_tensor=True)

    # Use cosine similarity to find the chunks most related to the topic
    cosine_scores = util.pytorch_cos_sim(topic_embedding, chunk_embeddings)[0]

    # Get the indices of the chunks sorted by their similarity score in descending order
    sorted_chunk_indices = torch.argsort(cosine_scores, descending=True)

    result = []

    for idx in sorted_chunk_indices[:10]:
        result.append(doc_chunks[idx.item()])

    return result


def gemini(text, doc):
    topic = topics_excavator(text)
    answer = getsentences(doc, topic)
    API_KEY = os.getenv("MY_API_KEY")
    genai.configure(api_key=API_KEY)

    gem = genai.GenerativeModel('gemini-pro')
    response = gem.generate_content(
        f"For the topics of {topic}, look at the following information found in our document related to {topic} and format it in a nice manner. For any relevant information to the topic, make sure your explanations are clear and precise. You can add some additional information that helps with understanding or is helpful for exam studying. Add details. Make everything is nicely formatted for a study guide: " + str(
            answer))
    print(response.text)
    return response.text
