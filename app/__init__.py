import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ensure required environment variables are set
if not os.getenv("OPENAI_API_KEY"):
    logging.warning("OPENAI_API_KEY not found in environment variables. LLM-based relevance filtering may not work.") 