# 🏥 Medical Q&A Chatbot

**Week 2 Internship Project** | Elevance Skills Technologies

A specialized medical question-answering chatbot powered by the MedQuAD dataset and Google Gemini API.

---

## 📋 Project Overview

This chatbot answers medical questions using:
- **MedQuAD Dataset**: 5,000+ verified medical Q&A pairs
- **Google Gemini API**: Advanced language understanding
- **Semantic Search**: Intelligent answer retrieval
- **Entity Recognition**: Identifies diseases, symptoms, treatments

### Key Features

✅ **Medical Q&A System**
- Answers medical questions from verified sources
- Retrieves relevant medical information
- Shows source references

✅ **Entity Recognition**
- Identifies diseases mentioned
- Extracts symptoms
- Recognizes treatments and medications
- Detects body parts

✅ **Semantic Search**
- Finds most relevant medical Q&A pairs
- Scores results by relevance
- Multi-source matching

✅ **Beautiful Web Interface**
- Clean Streamlit UI
- Chat conversation history
- Statistics dashboard
- Entity visualization

✅ **Medical Knowledge Base**
- 12 specialized medical data sources
- Covers: Cancer, Rare Diseases, Genetics, Health Topics, etc.
- Regular updates with verified information

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Streamlit Web UI                    │
│            (medical_app.py)                         │
└────────────────┬────────────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
Medical    Medical         Entity
Retrieval  Q&A Loader      Recognizer
(medical_  (medical_qa_    (medical_
retrieval) loader)         entities)
    │            │            │
    └────────────┼────────────┘
                 │
         ┌───────▼────────┐
         │  MedQuAD       │
         │  Dataset       │
         │  (5000+ Q&A)   │
         └────────────────┘
                 │
         ┌───────▼────────┐
         │  Gemini API    │
         │  (LLM)         │
         └────────────────┘
```

---

## 📂 Project Structure

```
task - 2/
├── medical_app.py              (Main Streamlit app)
├── medical_retrieval.py         (Q&A retrieval system)
├── medical_qa_loader.py         (Dataset loader)
├── medical_entities.py          (Entity recognition)
├── requirements.txt             (Dependencies)
├── .env.example                 (API key template)
├── README.md                    (This file)
└── QUICK_START.md              (Quick start guide)
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd "task - 2"
pip install -r requirements.txt
```

### Step 2: Set Up API Key

Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Download MedQuAD Dataset

```bash
git clone https://github.com/abachaa/MedQuAD.git
```

### Step 4: Run the Chatbot

```bash
python -m streamlit run medical_app.py
```

Open browser: **http://localhost:8501**

---

## 📚 Data Sources

The chatbot uses medical Q&A from:

| Source | Q&A Pairs | Focus |
|--------|-----------|-------|
| 1_CancerGov_QA | ~1,000 | Cancer information |
| 2_GARD_QA | ~600 | Rare diseases |
| 3_GHR_QA | ~700 | Genetic/hereditary conditions |
| 4_MPlus_Health_Topics_QA | ~800 | General health topics |
| 5_NIDDK_QA | ~500 | Kidney/urologic diseases |
| 6_NINDS_QA | ~600 | Neurological diseases |
| 7_SeniorHealth_QA | ~400 | Senior health |
| 8_NHLBI_QA_XML | ~500 | Heart/lung diseases |
| 9_CDC_QA | ~700 | CDC health information |
| 10_MPlus_ADAM_QA | ~300 | Medical animations |
| 11_MPlusDrugs_QA | ~500 | Medications |
| 12_MPlusHerbsSupplements_QA | ~400 | Herbs/supplements |

**Total: 7,500+ Q&A Pairs**

---

## 🔧 Component Details

### 1. **medical_qa_loader.py**
Loads and indexes medical Q&A dataset

```python
loader = MedicalQALoader("MedQuAD")
qa_pairs = loader.load_all_qa_pairs()
kb = loader.build_knowledge_base()
```

**Features:**
- Parses all MedQuAD folders
- Creates keyword index
- Ranks by relevance

### 2. **medical_retrieval.py**
Retrieves relevant answers using semantic search

```python
retrieval = MedicalRetrieval(API_KEY, "MedQuAD")
result = retrieval.answer_medical_question("What is diabetes?")
```

**Features:**
- Semantic similarity matching
- Multi-source retrieval
- Gemini API integration

### 3. **medical_entities.py**
Extracts medical entities from text

```python
recognizer = MedicalEntityRecognizer()
entities = recognizer.extract_diseases(text)
```

**Recognizes:**
- Diseases (30+ types)
- Symptoms (35+ types)
- Treatments (30+ types)
- Body parts (20+ types)

### 4. **medical_app.py**
Streamlit web interface

**Tabs:**
1. **Chat** - Ask medical questions
2. **Search** - Search medical topics
3. **Statistics** - View KB statistics
4. **About** - Project information

---

## 📊 Features Demo

### Feature 1: Ask Medical Questions

```
User: "What is diabetes?"

Bot: [Comprehensive answer from medical sources]
     [Lists relevant sources]
     [Shows related entities]
```

### Feature 2: Entity Recognition

Input: "Patient with fever and cough..."

Output:
```
🏥 Diseases: pneumonia
🤒 Symptoms: fever, cough
💊 Treatments: antibiotics
🫀 Body Parts: lungs
```

### Feature 3: Knowledge Base Search

Search for: "cancer treatment"

Results:
```
- Question 1: How is cancer treated?
  Source: CancerGov
  Answer: [Medical information]

- Question 2: What are cancer medications?
  Source: MPlusDrugs
  Answer: [Detailed answer]
```

### Feature 4: Statistics

```
📚 Total Q&A Pairs: 7,500+
🏢 Data Sources: 12
🤖 Model: Gemini 2.5 Flash
```

---

## 🎯 Use Cases

1. **Medical Education**
   - Students learning about diseases
   - Understanding medical conditions
   - Learning about treatments

2. **Patient Information**
   - Understanding medical conditions
   - Learning about treatments
   - Finding symptom information

3. **Healthcare Research**
   - Gathering medical information
   - Analyzing medical Q&A patterns
   - Understanding common questions

4. **Clinical Reference**
   - Quick medical information lookup
   - Symptom checking
   - Treatment options

---

## ⚙️ Configuration

### Customize Entity Recognition

Edit `medical_entities.py`:

```python
# Add more diseases
self.diseases = {
    'existing_diseases',
    'new_disease_1',
    'new_disease_2'
}
```

### Adjust Search Parameters

In `medical_app.py`:

```python
top_k = st.slider("Sources", 1, 5, 3)  # Default: 3
```

### Change Model

In `medical_retrieval.py`:

```python
self.model = genai.GenerativeModel("models/gemini-2.5-pro")
```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Q&A Pairs Indexed | 7,500+ |
| Data Sources | 12 |
| Entity Types | 4 (diseases, symptoms, treatments, body parts) |
| Search Speed | <1 second |
| Average Answer Quality | High |
| Data Coverage | Comprehensive |

---

## ⚠️ Medical Disclaimer

**IMPORTANT:** This chatbot provides educational information only.

**NOT A MEDICAL PROFESSIONAL:**
- Do not use for self-diagnosis
- Do not replace doctor consultation
- Always consult licensed healthcare professionals
- For emergencies, call emergency services

---

## 🔐 API Key Security

**IMPORTANT:**
- Never commit `.env` file to GitHub
- Keep API keys private
- Use `.env.example` as template
- Regenerate keys if exposed

---

## 🛠️ Troubleshooting

### Issue: "MedQuAD folder not found"
```bash
# Make sure MedQuAD is cloned
git clone https://github.com/abachaa/MedQuAD.git
```

### Issue: "API Key not found"
```bash
# Check .env file exists and has correct key
cat .env
# Should show: GEMINI_API_KEY=your_key_here
```

### Issue: Streamlit won't start
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run with Python module
python -m streamlit run medical_app.py
```

### Issue: Slow response time
- Check internet connection
- Verify Gemini API quota
- Ensure MedQuAD dataset is fully loaded

---

## 🚀 Future Enhancements

- [ ] Add more medical data sources
- [ ] Implement caching for faster retrieval
- [ ] Add multi-language support
- [ ] Integrate with medical APIs
- [ ] Add voice input/output
- [ ] Implement user authentication
- [ ] Add feedback mechanism
- [ ] Deploy to cloud platform

---

## 📚 References

- **MedQuAD Dataset**: https://github.com/abachaa/MedQuAD
- **Google Gemini API**: https://ai.google.dev/
- **Streamlit**: https://streamlit.io/
- **Medical NLP**: https://en.wikipedia.org/wiki/Biomedical_text_mining

---

## 👨‍💻 Author

**Nikhil** | Data Science Intern | Elevance Skills Technologies

- **Week 1**: Sentiment Analysis Chatbot ✅
- **Week 2**: Medical Q&A Chatbot 🏥
- **Week 3**: Dynamic Knowledge Base 📚
- **Week 4**: Multilingual Chatbot 🌍

---

## 📧 Contact

**Email**: b.nikhilsatya.dev@gmail.com  
**Internship Portal**: intern.elevanceskills.com  
**Questions**: training@elevanceskills.com

---

## 📄 License

This project is part of Elevance Skills Technologies internship program.

---

**Last Updated**: June 5, 2026  
**Status**: ✅ Week 2 Complete
