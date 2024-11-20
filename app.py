import streamlit as st
from educhain import Educhain
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def generate_questions(text, num_questions, instructions):
    """Generate questions from given text"""
    client = Educhain()
    try:
        questions = client.qna_engine.generate_questions_from_data(
            source=text,
            num=num_questions,
            custom_instructions=instructions,
            source_type="text"
        )
        return questions
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Question Generator", layout="wide")
    
    # Title and description
    st.title("📚 Educational Question Generator from content")
    st.markdown("""
    This app generates multiple-choice questions from your text content.
    Paste your text below and specify how many questions you'd like to generate.
    """)
    
    # Default instructions
    default_instructions = """Focus on Key Concepts:
Extract the main ideas and technical concepts discussed in the transcript
Avoid Context-Specific References:
Do not include questions tied to the video or module itself. Instead, create questions that are conceptually relevant and independent of the video context.
Encourage Application and Understanding:
Frame questions to encourage understanding of concepts and their applications
Diverse Question Types:
Include a variety of question types, such as:
Conceptual: What are the key components of a chatbot?
Analytical: How does memory improve user experience in chatbots?
Comparative: How are chatbots with internet functionality different from regular chatbots?
Avoid Repetition:
Ensure each question is unique and covers different aspects of the transcript.
Generalize Use Cases:
When referencing use cases, frame them in a broader context
Maintain Clarity:
Keep questions clear, concise, and relevant to the transcript's concepts.
Focus on Learning Objectives:
Ensure questions align with learning objectives such as understanding chatbots, their components, their features, and their use in generative AI applications."""
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input area
        text_input = st.text_area(
            "Paste your text here: or enter (Transcription of a Video)",
            height=300,
            placeholder="Enter the text from which you want to generate questions...(transcript)"
        )
    
    with col2:
        # Configuration options
        st.subheader("Configuration")
        num_questions = st.number_input(
            "Number of questions to generate:",
            min_value=1,
            max_value=20,
            value=5
        )
        
        # Optional: Allow users to modify instructions
        show_instructions = st.checkbox("Show/Edit Instructions")
        if show_instructions:
            instructions = st.text_area(
                "Custom Instructions:",
                value=default_instructions,
                height=300
            )
        else:
            instructions = default_instructions
            
        # Generate button
        generate_button = st.button("Generate Questions")
    
    # Progress information
    progress_placeholder = st.empty()
    questions_placeholder = st.container()
    
    if generate_button and text_input:
        with progress_placeholder:
            with st.spinner("Generating questions... This may take a minute."):
                questions = generate_questions(text_input, num_questions, instructions)
                
        with questions_placeholder:
            if questions:
                st.success("✅ Questions generated successfully!")
                
                # Create a formatted display of the questions
                with st.expander("View Generated Questions", expanded=True):
                    # Capture the output of questions.show()
                    import io
                    import sys
                    output = io.StringIO()
                    original_stdout = sys.stdout
                    sys.stdout = output
                    questions.show()
                    sys.stdout = original_stdout
                    questions_text = output.getvalue()
                    
                    # Display the questions in a nice format
                    st.code(questions_text, language='text')
                
                # Download button for generated questions
                st.download_button(
                    label="Download Questions",
                    data=str(questions.json()),
                    file_name="generated_questions.json",
                    mime="application/json"
                )
    
    # Instructions at the bottom
    with st.expander("How to use this app"):
        st.markdown("""
        1. **Paste your text**: Copy and paste the content you want to generate questions from in the text area
        2. **Configure options**: 
           - Set the number of questions you want to generate
           - Optionally modify the generation instructions
        3. **Generate**: Click the 'Generate Questions' button
        4. **Review**: Check the generated questions and their answers
        5. **Download**: Use the download button to save the questions for later use
        
        **Note**: The generation process may take a minute or two depending on the length of your text and the number of questions requested.
        """)

if __name__ == "__main__":
    main()
