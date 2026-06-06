import streamlit as st
import os
from dotenv import load_dotenv
from medical_retrieval import MedicalRetrieval
from medical_entities import MedicalEntityRecognizer

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Medical Q&A Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    .source-box {
        padding: 10px;
        background-color: #e8f4f8;
        border-radius: 5px;
        margin: 5px 0;
    }
    .entity-tag {
        background-color: #2d3748;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        display: inline-block;
        border: 1px solid #4a5568;
    }
    .answer-box{
    padding:15px;
    border-radius:10px;
    background-color:#1e293b;
    border:1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "retrieval" not in st.session_state:
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        st.error("❌ GEMINI_API_KEY not found! Please set your API key.")
        st.stop()
    
    with st.spinner("📚 Loading Medical Knowledge Base..."):
        st.session_state.retrieval = MedicalRetrieval(API_KEY, "MedQuAD")
    st.session_state.entity_recognizer = MedicalEntityRecognizer()
    st.session_state.messages = []
    st.session_state.entity_stats = {"diseases": 0, "symptoms": 0, "treatments": 0}

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🏥")
with col2:
    st.markdown("# Medical Q&A Chatbot")

st.markdown("*Get medical information from verified medical sources*")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Search Medical Topics", "📊 Statistics", "ℹ️ About"])

# ========== TAB 1: CHAT ==========
with tab1:
    st.subheader("Ask a Medical Question")
    
    # Sidebar for chat settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        use_entities = st.checkbox("Show Medical Entities", value=True)
        show_sources = st.checkbox("Show Source Information", value=True)
        top_k = st.slider("Number of sources to use", 1, 5, 3)
    
    # Chat input
    user_question = st.text_input(
        "Enter your medical question:",
        placeholder="e.g., What is diabetes? How is it treated?",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        submit = st.button("🔍 Ask Question", use_container_width=True)
    with col2:
        clear = st.button("🗑️ Clear", use_container_width=True)
    
    if clear:
        st.session_state.messages = []
        st.rerun()
    
    if submit and user_question:
        # Show loading spinner
        with st.spinner("🤔 Searching medical knowledge base..."):
            # Get answer
            result = st.session_state.retrieval.answer_medical_question(
                user_question, 
                use_context=True
            )
            
            # Extract entities
            if use_entities:
                entity_analysis = st.session_state.entity_recognizer.analyze_medical_text(
                    result['answer']
                )
        
        # Add to message history
        st.session_state.messages.append({
            'question': user_question,
            'answer': result['answer'],
            'sources': result['retrieved_sources'],
            'entities': entity_analysis if use_entities else None
        })
    
    # Display conversation
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("📋 Conversation History")
        
        for i, msg in enumerate(st.session_state.messages):
            with st.container():
                st.markdown(f"### ❓ Q{i+1}: {msg['question']}")
                
                # Answer
                st.markdown(f"""
                    <div style="
                    background:#111827;
                    padding:20px;
                    border-radius:12px;
                    border-left:5px solid #22c55e;
                    margin-bottom:15px;
                    ">
                    <h4>🤖 Medical Answer</h4>
                    <p>{msg['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Entities
                if use_entities and msg['entities']:
                    st.markdown("#### 🏷️ Medical Entities Found:")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        entities = msg['entities']['diseases']['recognized_diseases']
                        if entities:
                            st.markdown("**🏥 Diseases:**")
                            for entity in entities[:3]:
                                st.markdown(f"<span class='entity-tag'>{entity}</span>", 
                                           unsafe_allow_html=True)
                    
                    with col2:
                        entities = msg['entities']['symptoms']['recognized_symptoms']
                        if entities:
                            st.markdown("**🤒 Symptoms:**")
                            for entity in entities[:3]:
                                st.markdown(f"<span class='entity-tag'>{entity}</span>", 
                                           unsafe_allow_html=True)
                    
                    with col3:
                        entities = msg['entities']['treatments']['recognized_treatments']
                        if entities:
                            st.markdown("**💊 Treatments:**")
                            for entity in entities[:3]:
                                st.markdown(f"<span class='entity-tag'>{entity}</span>", 
                                           unsafe_allow_html=True)
                
                # Sources
                if show_sources and msg['sources']:
                    st.markdown("#### 📚 Medical Sources Used:")
                    for j, source in enumerate(msg['sources'], 1):
                        with st.expander(f"Source {j}: {source['source']}"):
                            st.markdown(f"**Related Question:** {source['related_question']}")
                            st.markdown(f"**Relevance Score:** {source['relevance_score']}/10")
                
                st.markdown("---")
        
        # Summary stats
        st.subheader("📊 Session Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions Asked", len(st.session_state.messages))
        with col2:
            st.metric("Sources Used", sum(len(m.get('sources', [])) for m in st.session_state.messages))
        with col3:
            st.metric("Total Answers", len(st.session_state.messages))

# ========== TAB 2: SEARCH ==========
with tab2:
    st.subheader("🔍 Search Medical Topics")
    
    search_topic = st.text_input(
        "Search for medical topic:",
        placeholder="e.g., cancer, diabetes, heart disease",
        label_visibility="collapsed"
    )
    
    num_results = st.slider("Number of results", 1, 10, 5)
    
    if search_topic:
        with st.spinner(f"Searching for '{search_topic}'..."):
            results = st.session_state.retrieval.search_by_medical_topic(
                search_topic, 
                top_k=num_results
            )
        
        if results:
            st.success(f"Found {len(results)} results for '{search_topic}'")
            
            for i, result in enumerate(results, 1):
                with st.expander(f"{i}. {result['question'][:60]}..."):
                    st.markdown(f"**Source:** {result['source']}")
                    st.markdown(f"**Answer:** {result['answer']}")
        else:
            st.warning(f"No results found for '{search_topic}'")

# ========== TAB 3: STATISTICS ==========
with tab3:
    st.subheader("📊 Medical Knowledge Base Statistics")
    
    stats = st.session_state.retrieval.get_statistics()
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Q&A Pairs", f"{stats['total_qa_pairs']:,}")
    with col2:
        st.metric("🏢 Data Sources", stats['total_sources'])
    with col3:
        st.metric("🤖 Model Used", stats['model_used'])
    
    st.markdown("---")
    
    # Sources breakdown
    st.subheader("📈 Q&A Pairs by Source")
    
    sources = stats['sources_breakdown']
    
    # Create columns for each source
    num_cols = min(3, len(sources))
    cols = st.columns(num_cols)
    
    for idx, (source, count) in enumerate(sources.items()):
        with cols[idx % num_cols]:
            st.metric(source, f"{count} pairs")
    
    # Display as bar chart
    import pandas as pd
    
    df = pd.DataFrame(list(sources.items()), columns=['Source', 'Q&A Pairs'])
    st.bar_chart(df.set_index('Source'))

# ========== TAB 4: ABOUT ==========
with tab4:
    st.subheader("ℹ️ About Medical Q&A Chatbot")
    
    st.markdown("""
    ### 🏥 Features
    - **Medical Q&A System**: Answers medical questions using verified medical sources
    - **MedQuAD Dataset**: Powered by 5,000+ medical Q&A pairs
    - **Semantic Search**: Intelligent matching for relevant answers
    - **Entity Recognition**: Identifies diseases, symptoms, and treatments
    - **Source Tracking**: Shows which medical sources were used
    - **Beautiful Interface**: Easy-to-use web interface
    
    ### 📚 Data Sources
    - CancerGov - Cancer information
    - GARD - Rare disease database
    - GHR - Genetic and hereditary information
    - CDC - General health information
    - MPlus - Health topics
    - NIDDK - Kidney and urologic diseases
    - NINDS - Neurological diseases
    - And more...
    
    ### ⚠️ Medical Disclaimer
    This chatbot provides educational information only. 
    **Always consult with a licensed healthcare professional for medical advice.**
    
    ### 🛠️ Technology
    - **Language Model**: Google Gemini 2.5 Flash
    - **Framework**: Streamlit
    - **Knowledge Base**: MedQuAD Dataset
    - **NLP**: Text analysis and entity recognition
    
    ### 📧 Information
    - **Dataset**: https://github.com/abachaa/MedQuAD
    - **Framework**: Streamlit
    - **AI Model**: Google Gemini API
    """)
    
    st.markdown("---")
    st.markdown("**Week 2 Project:** Medical Q&A Chatbot | Elevance Skills Internship")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏥 Medical Q&A Chatbot | Powered by Gemini API & MedQuAD Dataset</p>
    <p style='font-size: 12px; color: gray;'>⚠️ For educational purposes only. Always consult healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)
