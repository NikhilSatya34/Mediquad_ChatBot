"""
Medical Q&A Loader
Loads and processes MedQuAD dataset from all folders
Creates searchable medical knowledge base
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple


class MedicalQALoader:
    """
    Loads medical Q&A pairs from MedQuAD dataset
    Organizes by source and creates indexed knowledge base
    """
    
    def __init__(self, medquad_path: str = "MedQuAD"):
        """Initialize loader with path to MedQuAD folder"""
        self.medquad_path = medquad_path
        self.qa_pairs = []
        self.sources = {}
        self.knowledge_base = {}
        
    def load_all_qa_pairs(self) -> List[Dict]:
        """
        Load Q&A pairs from all MedQuAD source folders
        
        Returns:
            List of Q&A pair dictionaries
        """
        print("📚 Loading MedQuAD Dataset...\n")
        
        medquad_dir = Path(self.medquad_path)
        
        if not medquad_dir.exists():
            print(f"❌ Error: {self.medquad_path} folder not found!")
            return []
        
        # Get all source folders
        source_folders = sorted([
            f for f in medquad_dir.iterdir() 
            if f.is_dir() and not f.name.startswith('.')
        ])
        
        total_qa_pairs = 0
        
        for source_folder in source_folders:
            source_name = source_folder.name
            source_qa_count = 0
            
            # Process all files in the source folder
            for file_path in source_folder.rglob("*.xml"):
                try:
                    qa_pair = self._parse_qa_file(file_path, source_name)
                    if qa_pair:
                        self.qa_pairs.extend(qa_pair)
                        source_qa_count += len(qa_pair)
                except Exception as e:
                    print(f"⚠️ Error processing {file_path}: {str(e)}")
            
            if source_qa_count > 0:
                self.sources[source_name] = source_qa_count
                total_qa_pairs += source_qa_count
                print(f"✅ {source_name}: {source_qa_count} Q&A pairs")
        
        print(f"\n📊 Total Q&A pairs loaded: {total_qa_pairs}\n")
        return self.qa_pairs
    
    import xml.etree.ElementTree as ET

    def _parse_qa_file(self, file_path, source):
        qa_pairs = []

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for qa in root.findall(".//QAPair"):

                question_elem = qa.find("Question")
                answer_elem = qa.find("Answer")

                question = ""
                answer = ""

                if question_elem is not None:
                    question = "".join(question_elem.itertext()).strip()

                if answer_elem is not None:
                    answer = "".join(answer_elem.itertext()).strip()

                if question:
                    qa_pairs.append({
                        "question": question,
                        "answer": answer,
                        "source": source,
                        "file": str(file_path),
                        "question_lower": question.lower()
                    })

            return qa_pairs

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []
        
    def build_knowledge_base(self) -> Dict:
        """
        Build indexed knowledge base for fast retrieval
        
        Returns:
            Dictionary with indexed Q&A pairs
        """
        print("🔍 Building Knowledge Base Index...\n")
        
        # Index by keywords from questions
        self.knowledge_base = {
            'all_qa_pairs': self.qa_pairs,
            'sources': self.sources,
            'total_pairs': len(self.qa_pairs),
            'indexed_by_keyword': self._index_by_keywords()
        }
        
        print(f"✅ Knowledge base ready!")
        print(f"   - Total Q&A pairs: {len(self.qa_pairs)}")
        print(f"   - Sources: {len(self.sources)}")
        return self.knowledge_base
    
    def _index_by_keywords(self) -> Dict:
        """Create keyword index for fast searching"""
        keyword_index = {}
        
        for idx, qa_pair in enumerate(self.qa_pairs):
            # Extract keywords from question
            words = qa_pair['question_lower'].split()
            
            # Index important words (> 3 chars)
            for word in words:
                clean_word = word.strip('.,!?;:')
                if len(clean_word) > 3:
                    if clean_word not in keyword_index:
                        keyword_index[clean_word] = []
                    keyword_index[clean_word].append(idx)
        
        return keyword_index
    
    def search_by_keyword(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for medical Q&A by keyword
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant Q&A pairs
        """
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Score each Q&A pair
        scores = {}
        
        for idx, qa_pair in enumerate(self.qa_pairs):
            score = 0
            
            # Match keywords
            for word in query_words:
                if len(word) > 3 and word in qa_pair['question_lower']:
                    score += 2  # Question match worth more
                if len(word) > 3 and word in qa_pair['answer'].lower():
                    score += 1
            
            if score > 0:
                scores[idx] = score
        
        # Sort by score and return top results
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_results = [self.qa_pairs[idx] for idx, _ in sorted_results[:top_k]]
        
        return top_results
    
    def get_all_diseases(self) -> List[str]:
        """Extract list of diseases from Q&A pairs"""
        diseases = set()
        
        disease_keywords = ['disease', 'cancer', 'diabetes', 'heart', 'syndrome', 
                           'disorder', 'condition', 'infection', 'virus', 'bacteria']
        
        for qa_pair in self.qa_pairs:
            question_lower = qa_pair['question_lower']
            
            for keyword in disease_keywords:
                if keyword in question_lower:
                    # Extract words around keyword
                    words = question_lower.split()
                    idx = words.index(keyword) if keyword in words else -1
                    if idx > 0:
                        potential_disease = words[idx-1]
                        if len(potential_disease) > 2:
                            diseases.add(potential_disease)
        
        return sorted(list(diseases))
    
    def get_sources_summary(self) -> Dict:
        """Get summary of data from each source"""
        return {
            'total_sources': len(self.sources),
            'sources_detail': self.sources,
            'total_qa_pairs': len(self.qa_pairs)
        }


# Example usage
if __name__ == "__main__":
    # Load MedQuAD dataset
    loader = MedicalQALoader("MedQuAD")
    qa_pairs = loader.load_all_qa_pairs()
    
    # Build knowledge base
    kb = loader.build_knowledge_base()
    
    # Get summary
    summary = loader.get_sources_summary()
    print("\n" + "="*70)
    print("MEDICAL KNOWLEDGE BASE SUMMARY")
    print("="*70)
    print(f"Total Q&A Pairs: {summary['total_qa_pairs']}")
    print(f"Data Sources: {summary['total_sources']}")
    print("\n📊 Breakdown by Source:")
    for source, count in summary['sources_detail'].items():
        print(f"  - {source}: {count} pairs")
    
    # Test search
    print("\n" + "="*70)
    print("TESTING SEARCH FUNCTIONALITY")
    print("="*70)
    
    test_queries = [
        "What is diabetes?",
        "Heart disease symptoms",
        "Cancer treatment"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = loader.search_by_keyword(query, top_k=2)
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"  Q: {result['question'][:80]}...")
            print(f"  Source: {result['source']}")
