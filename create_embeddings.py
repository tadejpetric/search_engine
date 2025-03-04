from typing import Optional
import numpy as np
from openai import OpenAI


def get_embeddings(question: str, client: OpenAI) -> Optional[np.ndarray]:
    try:
        # Call the Gemini 2.0 Flash model via the OpenAI API
        response = client.embeddings.create(
            model="text-embedding-004",
            input=question,
        )

        # Extract the summary from the response
        return np.array(response.data[0].embedding)

    except Exception as e:
        print(f"An error occurred processing '{question}': {e}")
        return None