"""
Medical Entity Recognition
Extracts medical entities: diseases, symptoms, treatments
Uses pattern matching and keyword recognition
"""

from typing import List, Dict, Set
import re


class MedicalEntityRecognizer:
    """
    Recognizes and extracts medical entities from text
    Identifies: diseases, symptoms, treatments, medications
    """
    
    def __init__(self):
        """Initialize with medical entity dictionaries"""
        # Common diseases
        self.diseases = {
            'diabetes', 'cancer', 'heart disease', 'hypertension', 'asthma',
            'arthritis', 'tuberculosis', 'pneumonia', 'stroke', 'alzheimer',
            'parkinson', 'epilepsy', 'migraine', 'depression', 'anxiety',
            'schizophrenia', 'autism', 'eczema', 'psoriasis', 'alopecia',
            'hepatitis', 'hiv', 'aids', 'covid', 'influenza', 'malaria',
            'obesity', 'anemia', 'osteoporosis', 'glaucoma', 'cataracts'
        }
        
        # Common symptoms
        self.symptoms = {
            'fever', 'cough', 'headache', 'fatigue', 'pain', 'nausea',
            'vomiting', 'diarrhea', 'constipation', 'shortness of breath',
            'chest pain', 'dizziness', 'weakness', 'chills', 'sore throat',
            'runny nose', 'congestion', 'muscle ache', 'joint pain',
            'rash', 'itching', 'burning', 'numbness', 'tingling',
            'tremor', 'loss of appetite', 'insomnia', 'irritability',
            'anxiety', 'confusion', 'memory loss', 'vision problems'
        }
        
        # Common treatments and medications
        self.treatments = {
            'surgery', 'chemotherapy', 'radiation', 'therapy', 'medication',
            'antibiotic', 'pain reliever', 'anti-inflammatory', 'vaccine',
            'insulin', 'aspirin', 'ibuprofen', 'paracetamol', 'amoxicillin',
            'penicillin', 'antiviral', 'antihistamine', 'corticosteroid',
            'beta blocker', 'statin', 'acupuncture', 'physical therapy',
            'cognitive behavioral therapy', 'counseling', 'meditation'
        }
        
        # Body parts
        self.body_parts = {
            'heart', 'lung', 'brain', 'liver', 'kidney', 'pancreas',
            'stomach', 'intestine', 'bone', 'muscle', 'skin', 'eye',
            'ear', 'nose', 'throat', 'arm', 'leg', 'hand', 'foot',
            'head', 'spine', 'blood vessel', 'nerve', 'joint'
        }
    
    def extract_diseases(self, text: str) -> Dict[str, List[str]]:
        """
        Extract disease mentions from text
        
        Args:
            text: Medical text
            
        Returns:
            Dictionary with recognized and potential diseases
        """
        text_lower = text.lower()
        recognized = []
        
        # Find recognized diseases
        for disease in self.diseases:
            if disease in text_lower:
                recognized.append(disease)
        
        # Find potential diseases (common patterns)
        disease_patterns = [
            r'\b[A-Z][a-z]+\s+syndrome\b',  # e.g., "Marfan syndrome"
            r'\b[A-Z][a-z]+\s+disease\b',   # e.g., "Crohn disease"
            r'\b[A-Z][a-z]+\s+disorder\b'   # e.g., "Bipolar disorder"
        ]
        
        potential = []
        for pattern in disease_patterns:
            matches = re.findall(pattern, text)
            potential.extend(matches)
        
        return {
            'recognized_diseases': list(set(recognized)),
            'potential_diseases': list(set(potential)),
            'total_found': len(set(recognized)) + len(set(potential))
        }
    
    def extract_symptoms(self, text: str) -> Dict[str, List[str]]:
        """
        Extract symptom mentions from text
        
        Args:
            text: Medical text
            
        Returns:
            Dictionary with recognized and potential symptoms
        """
        text_lower = text.lower()
        recognized = []
        
        # Find recognized symptoms
        for symptom in self.symptoms:
            if symptom in text_lower:
                recognized.append(symptom)
        
        # Find potential symptoms (common patterns)
        symptom_patterns = [
            r'(?:experience|suffering from|complain of|report)\s+([a-z\s]+)',
            r'(?:symptom|signs?)\s+(?:of|include)\s+([a-z\s,]+)',
            r'patient\s+(?:presents?|shows?)\s+([a-z\s]+)'
        ]
        
        potential = []
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text_lower)
            potential.extend(matches)
        
        return {
            'recognized_symptoms': list(set(recognized)),
            'potential_symptoms': list(set(potential)),
            'total_found': len(set(recognized)) + len(set(potential))
        }
    
    def extract_treatments(self, text: str) -> Dict[str, List[str]]:
        """
        Extract treatment and medication mentions from text
        
        Args:
            text: Medical text
            
        Returns:
            Dictionary with recognized and potential treatments
        """
        text_lower = text.lower()
        recognized = []
        
        # Find recognized treatments
        for treatment in self.treatments:
            if treatment in text_lower:
                recognized.append(treatment)
        
        # Find potential treatments (common patterns)
        treatment_patterns = [
            r'(?:treat|manage|address)\s+(?:with|using)\s+([a-z\s]+)',
            r'(?:therapy|treatment)\s+(?:includes?|involves?)\s+([a-z\s,]+)',
            r'(?:prescribe|recommend|advise)\s+([a-z\s]+)'
        ]
        
        potential = []
        for pattern in treatment_patterns:
            matches = re.findall(pattern, text_lower)
            potential.extend(matches)
        
        return {
            'recognized_treatments': list(set(recognized)),
            'potential_treatments': list(set(potential)),
            'total_found': len(set(recognized)) + len(set(potential))
        }
    
    def extract_body_parts(self, text: str) -> Dict[str, List[str]]:
        """
        Extract body part mentions from text
        
        Args:
            text: Medical text
            
        Returns:
            Dictionary with mentioned body parts
        """
        text_lower = text.lower()
        mentioned = []
        
        for body_part in self.body_parts:
            if body_part in text_lower:
                mentioned.append(body_part)
        
        return {
            'body_parts': list(set(mentioned)),
            'total_found': len(set(mentioned))
        }
    
    def analyze_medical_text(self, text: str) -> Dict:
        """
        Comprehensive analysis of medical text
        Extracts all entity types
        
        Args:
            text: Medical text to analyze
            
        Returns:
            Dictionary with all extracted entities
        """
        return {
            'original_text': text[:200] + "..." if len(text) > 200 else text,
            'diseases': self.extract_diseases(text),
            'symptoms': self.extract_symptoms(text),
            'treatments': self.extract_treatments(text),
            'body_parts': self.extract_body_parts(text),
            'text_length': len(text)
        }
    
    def get_entity_summary(self, text: str) -> str:
        """
        Get a summary of entities found in text
        
        Args:
            text: Medical text
            
        Returns:
            Human-readable summary
        """
        analysis = self.analyze_medical_text(text)
        
        summary = "📋 Medical Entity Summary:\n\n"
        
        # Diseases
        diseases = analysis['diseases']['recognized_diseases']
        if diseases:
            summary += f"🏥 Diseases Found: {', '.join(diseases)}\n"
        
        # Symptoms
        symptoms = analysis['symptoms']['recognized_symptoms']
        if symptoms:
            summary += f"🤒 Symptoms Found: {', '.join(symptoms)}\n"
        
        # Treatments
        treatments = analysis['treatments']['recognized_treatments']
        if treatments:
            summary += f"💊 Treatments Found: {', '.join(treatments)}\n"
        
        # Body parts
        body_parts = analysis['body_parts']['body_parts']
        if body_parts:
            summary += f"🫀 Body Parts: {', '.join(body_parts)}\n"
        
        if not (diseases or symptoms or treatments or body_parts):
            summary += "No medical entities found in the text."
        
        return summary


# Example usage
if __name__ == "__main__":
    recognizer = MedicalEntityRecognizer()
    
    # Test medical text
    test_text = """
    Patient presents with fever and cough for 3 days. Physical examination reveals
    chest pain and shortness of breath. Diagnosis: Pneumonia. Treatment involves
    antibiotics and rest. The patient has a history of asthma and diabetes.
    """
    
    print("🏥 Medical Entity Recognition\n")
    print("="*70)
    print(f"Input Text:\n{test_text}\n")
    print("="*70)
    
    # Analyze
    analysis = recognizer.analyze_medical_text(test_text)
    
    print("\n📊 Analysis Results:\n")
    print(f"Diseases: {analysis['diseases']['recognized_diseases']}")
    print(f"Symptoms: {analysis['symptoms']['recognized_symptoms']}")
    print(f"Treatments: {analysis['treatments']['recognized_treatments']}")
    print(f"Body Parts: {analysis['body_parts']['body_parts']}")
    
    # Summary
    print("\n" + recognizer.get_entity_summary(test_text))
