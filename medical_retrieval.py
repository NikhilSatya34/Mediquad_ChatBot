from typing import List, Dict, Tuple
import google.generativeai as genai
from medical_qa_loader import MedicalQALoader
import textwrap

class MedicalRetrieval:
    """
    Retrieves relevant medical Q&A using semantic search
    Finds best matching answers to medical questions
    """
    
    def __init__(self, api_key: str, medquad_path: str = "MedQuAD"):
        """
        Initialize medical retrieval system
        
        Args:
            api_key: Gemini API key
            medquad_path: Path to MedQuAD dataset
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        # Load medical knowledge base
        print("📚 Loading Medical Knowledge Base...")
        self.loader = MedicalQALoader(medquad_path)
        self.qa_pairs = self.loader.load_all_qa_pairs()
        self.kb = self.loader.build_knowledge_base()
        
        if not self.qa_pairs:
            raise ValueError("❌ Failed to load MedQuAD dataset!")
        
        print(f"✅ Knowledge base ready with {len(self.qa_pairs)} Q&A pairs\n")
    
    def retrieve_relevant_answers(self, question: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant medical answers for a question
        
        Args:
            question: Medical question
            top_k: Number of top results to return
            
        Returns:
            List of relevant Q&A pairs
        """
        # First try keyword search
        keyword_results = self.loader.search_by_keyword(question, top_k=top_k*2)
        
        # Score and rank by relevance
        scored_results = self._score_relevance(question, keyword_results)
        
        # Return top results
        return scored_results[:top_k]
    
    def _score_relevance(self, question: str, candidates: List[Dict]) -> List[Dict]:
        """
        Score candidates by relevance to the question
        
        Args:
            question: User's medical question
            candidates: Candidate Q&A pairs
            
        Returns:
            Sorted list by relevance score
        """
        question_lower = question.lower()
        
        for candidate in candidates:
            score = 0
            
            # Exact keyword matches in question
            question_words = set(question_lower.split())
            candidate_words = set(candidate['question_lower'].split())
            
            common_words = len(question_words & candidate_words)
            score += common_words * 10
            
            # Partial matching
            if any(word in candidate['question_lower'] for word in question_lower.split()):
                score += 5
            
            candidate['relevance_score'] = score
        
        # Sort by relevance
        return sorted(candidates, key=lambda x: x['relevance_score'], reverse=True)
    
    def get_medical_context(self, question: str) -> str:
        """
        Get medical context from retrieved answers
        
        Args:
            question: Medical question
            
        Returns:
            Concatenated relevant answers as context
        """
        results = self.retrieve_relevant_answers(question, top_k=3)
        
        context = "RELEVANT MEDICAL INFORMATION:\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"Source {i} ({result['source']}):\n"
            context += f"Q: {result['question']}\n"
            context += f"A: {result['answer'][:200]}...\n\n"
        
        return context
    
    def answer_medical_question(self, question: str, use_context: bool = True) -> Dict:
        """
        Answer a medical question using Gemini + MedQuAD context
        
        Args:
            question: Medical question
            use_context: Whether to use retrieved medical context
            
        Returns:
            Dictionary with question, answer, and sources
        """
        # Retrieve relevant medical information
        retrieved = self.retrieve_relevant_answers(question, top_k=3)
        
        # Build prompt with medical context
        if use_context and retrieved:
            context = self.get_medical_context(question)
            prompt = f"""{context}

Based on the medical information above, answer this question:
{question}

Provide a helpful and accurate medical answer. If the retrieved sources don't fully answer the question, 
provide additional medical knowledge while being clear about what came from the sources."""
        else:
            prompt = f"""You are a medical information assistant. Answer this medical question accurately:
{question}

Note: Provide educational information only. Always recommend consulting healthcare professionals for medical advice."""
        
        try:
            response = self.model.generate_content(prompt)
            answer = response.text

        except Exception as e:
            if "429" in str(e):
                print("⚠️ Gemini quota exceeded. Using dataset.")
            else:
                print(f"⚠️ Error: {e}")

            if retrieved:
                answer = "📚 Information from verified medical sources:\n\n"

                best_result = retrieved[0]

                answer += f"""
        💡 Answer:
        {textwrap.shorten(best_result['answer'], width=500, placeholder='...')}
        """

            else:
                answer = f"⚠️ Error generating response: {str(e)}"
        return {
            'question': question,
            'answer': answer,
            'retrieved_sources': [
                {
                    'source': r['source'],
                    'related_question': r['question'],
                    'relevance_score': r.get('relevance_score', 0)
                }
                for r in retrieved
            ],
            'sources_used': len(retrieved)
        }
    
    def search_by_medical_topic(self, topic: str, top_k: int = 5) -> List[Dict]:
        """
        Search for Q&A related to a medical topic
        
        Args:
            topic: Medical topic to search
            top_k: Number of results
            
        Returns:
            Relevant Q&A pairs about the topic
        """
        return self.loader.search_by_keyword(topic, top_k=top_k)
    
    def get_disease_information(self, disease: str) -> Dict:
        """
        Get comprehensive information about a disease
        
        Args:
            disease: Disease name
            
        Returns:
            Information about the disease from medical sources
        """
        search_results = self.loader.search_by_keyword(disease, top_k=5)
        
        if not search_results:
            return {
                'disease': disease,
                'found': False,
                'message': f"No information found about {disease}"
            }
        
        # Compile information from multiple sources
        info_dict = {
            'disease': disease,
            'found': True,
            'sources': {},
            'qa_pairs': []
        }
        
        for result in search_results:
            source = result['source']
            if source not in info_dict['sources']:
                info_dict['sources'][source] = []
            
            info_dict['sources'][source].append({
                'question': result['question'],
                'answer': result['answer'][:300] + "..."
            })
            
            info_dict['qa_pairs'].append({
                'question': result['question'],
                'answer': result['answer'],
                'source': source
            })
        
        return info_dict
    
    def get_statistics(self) -> Dict:
        """Get statistics about the medical knowledge base"""
        sources_summary = self.loader.get_sources_summary()
        
        return {
            'total_qa_pairs': sources_summary['total_qa_pairs'],
            'total_sources': sources_summary['total_sources'],
            'sources_breakdown': sources_summary['sources_detail'],
            'model_used': 'Gemini 2.5 Flash',
            'knowledge_base': 'MedQuAD'
        }


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY") 
    print("🏥 Medical Q&A Retrieval System\n")
    print("="*70)
    
    # Initialize retrieval system
    retrieval = MedicalRetrieval(API_KEY, "MedQuAD")
    
    # Test questions
    test_questions = [
        "What is diabetes?",
        "How is heart disease treated?",
        "What are cancer symptoms?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("-" * 70)
        
        # Get answer
        result = retrieval.answer_medical_question(question)
        
        print(f"\n🤖 Answer:\n{result['answer'][:300]}...")
        print(f"\n📚 Sources used: {result['sources_used']}")
        
        for source in result['retrieved_sources']:
            print(f"  - {source['source']} (score: {source['relevance_score']})")
        print("="*70)
    
    # Get statistics
    print("\n📊 Knowledge Base Statistics:")
    stats = retrieval.get_statistics()
    print(f"  Total Q&A Pairs: {stats['total_qa_pairs']}")
    print(f"  Total Sources: {stats['total_sources']}")
    print(f"  Model: {stats['model_used']}")
