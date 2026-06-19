import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate the TF-IDF cosine similarity between a resume and a job description.
    
    Args:
        resume_text: The full text of the resume.
        jd_text: The full text of the job description.
        
    Returns:
        A score between 0.0 and 100.0 representing text similarity.
    """
    if not resume_text or not resume_text.strip() or not jd_text or not jd_text.strip():
        return 0.0
        
    try:
        # We use english stop words to ignore "and", "the", "is", etc.
        # ngram_range=(1, 2) allows us to capture bigrams like "machine learning" 
        # in the general text similarity, not just single words.
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        
        # Fit and transform the texts into a TF-IDF matrix
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        
        # Calculate cosine similarity between the resume (index 0) and JD (index 1)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to a percentage
        return round(similarity * 100, 2)
        
    except Exception as e:
        logger.error(f"Similarity calculation failed: {e}")
        return 0.0
