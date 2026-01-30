import streamlit as st
import sys
import os
import json

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from generate_testcases import generate_testcases_tool

st.set_page_config(
    page_title="Local LLM Testcase Generator",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for "Premium" feel (Dark mode is default in Streamlit)
st.markdown("""
    <style>
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        padding: 10px 24px;
    }
    .stButton button:hover {
        background-color: #FF2B2B;
        border-color: #FF2B2B;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar for constraints/settings
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox("Model", ["llama3.2", "llama3"], index=0)
    st.info("Ensure Ollama is running (`ollama serve`).")
    st.markdown("---")
    st.markdown("**Instructions:**\n1. Enter a feature description.\n2. Click Generate.\n3. Download the result.")

st.title("🧪 Local LLM Testcase Generator")
st.markdown("### Generate professional Gherkin test cases securely.")

# Input
prompt = st.text_area("Describe the feature to test:", height=150, placeholder="e.g., A login page with email and password fields, including 'Forgot Password' link.")

# Action
if st.button("Generate Test Cases", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a description first.")
    else:
        with st.spinner("🤖 Generating test cases... (this may take a moment)"):
            result = generate_testcases_tool(prompt, model=selected_model)
            
            try:
                # Attempt to find JSON content if wrapped in backticks
                content = result
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].strip()
                
                test_cases = json.loads(content)
                
                st.success(f"Generated {len(test_cases)} Test Cases!")
                
                # Render keys for data download
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(test_cases, indent=2),
                    file_name="test_cases.json",
                    mime="application/json"
                )

                # Custom Card Rendering
                for tc in test_cases:
                    # Badge Color
                    badge_color = "#28a745" if tc['type'].upper() == "POSITIVE" else "#dc3545"
                    
                    html_card = f"""
                    <div style="
                        background-color: #0E1117; 
                        border: 1px solid #30333D; 
                        border-radius: 8px; 
                        padding: 16px; 
                        margin-bottom: 16px; 
                        font-family: sans-serif;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="color: #9CACB4; font-size: 12px;">{tc['id']}</span>
                            <span style="
                                background-color: {badge_color}20; 
                                color: {badge_color}; 
                                padding: 2px 8px; 
                                border-radius: 4px; 
                                font-size: 11px; 
                                font-weight: bold; 
                                border: 1px solid {badge_color};">
                                {tc['type'].upper()}
                            </span>
                        </div>
                        <h3 style="color: #4da6ff; margin: 0 0 12px 0; font-size: 16px;">{tc['title']}</h3>
                        <div style="color: #E6E6E6; font-size: 14px; margin-bottom: 12px;">
                            <strong style="color: #9CACB4;">Steps:</strong>
                            <ol style="margin-top: 4px; padding-left: 20px;">
                                {''.join([f'<li style="margin-bottom: 4px;">{step}</li>' for step in tc['steps']])}
                            </ol>
                        </div>
                        <div style="color: #9CACB4; font-size: 13px; border-top: 1px solid #30333D; padding-top: 8px;">
                            Expected: <span style="color: #E6E6E6;">{tc['expected']}</span>
                        </div>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Error: The LLM did not return valid JSON. Showing raw output instead.")
                st.code(result, language="text")
            except Exception as e:
                st.error(f"Error parsing test cases: {str(e)}")
                st.code(result, language="text")

# Footer
st.markdown("---")
st.caption("Powered by Local LLM (Ollama) | Built with Streamlit")
