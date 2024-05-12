import os

import google.generativeai as genai
import getTextPDF
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(Path(".env"))


def format_topics(text):
    # Split the text into lines
    lines = text.splitlines()

    # Remove empty lines and lines starting with "* " (topics)
    formatted_lines = [line for line in lines if line and not line.startswith("* ")]

    # Remove leading spaces and colons from non-empty lines (subtopics)
    formatted_lines = [line.strip(': ') for line in formatted_lines]

    # Combine formatted lines back into a string
    formatted_text = "\n".join(formatted_lines)

    return formatted_text


def topics_excavator(text):
    GOOGLE_API_KEY = os.getenv("API_BACKUP")
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        "Extract the general topics from this text. Make sure it's only the global topics, not anything specific:: " + text)

    return format_topics(response.text)
