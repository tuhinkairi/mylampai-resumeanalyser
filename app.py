import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from llm_reviewer.agent import *
from llm_reviewer.brevity import *
from llm_reviewer.style import *
from llm_reviewer.impact import *
import tempfile
from utils.utils import *
import base64
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from streamlit_utils.custom_background import Background



colour_dict = {
    "green":(0.847, 0.988, 0.882),
    "blue":(0.725, 0.71, 0.988),
    "red":(1, 0.698, 0.698),
    "yellow":(1, 0.894, 0.698)
}



def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def get_path(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name
    return temp_file_path

def show_pdf_from_bytes(pdf_bytes):
    pdf_viewer(pdf_bytes,render_text=True)
    # base64_pdf = base64.b64encode(pdf_bytes.getvalue()).decode('utf-8')
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    bacground_img = Background()
    
    st.markdown(bacground_img.background_img_md(), unsafe_allow_html=True)
    
    st.title("Resume Analyzer")
    uploaded_file = st.file_uploader("Upload your CV (PDF)", type="pdf")

    if uploaded_file:
        if 'cv_text' not in st.session_state:
            st.session_state.cv_text = extract_text_from_pdf(uploaded_file)
        
        if st.session_state.cv_text:
            st.success("CV uploaded successfully!")
            
            if 'structured_data' not in st.session_state:
                st.session_state.structured_data = extract_structured_data(st.session_state.cv_text)
            
            if 'analysis_results' not in st.session_state:
                st.session_state.analysis_results = {}
            
            if 'highlighted_pdfs' not in st.session_state:
                st.session_state.highlighted_pdfs = {}
            
            st.sidebar.header("Analysis Functions")

            analysis_functions = {
                "Quantification Checker": lambda: quantification("\n".join(st.session_state.structured_data["Description"])),
                "Resume Length": lambda: resume_length(st.session_state.cv_text),
                "Bullet Point Length": lambda: bullet_point_length(st.session_state.structured_data["Description"]),
                "Bullet Points Improver": lambda: bullet_points_improver("\n".join(st.session_state.structured_data["Description"])),
                "Total Bullet Points": lambda: total_bullet_list(st.session_state.structured_data["Description"]),
                "Personal Info": lambda: personal_info(st.session_state.structured_data["Personal Information"]),
                "Weak Verb Checker": lambda: weak_verb_checker("\n".join(st.session_state.structured_data["Description"])),
                "Section Checker": lambda: section_checker(st.session_state.structured_data["Sections"]),
                "Skill Checker": lambda: skill_checker(st.session_state.structured_data["Skills"]["HARD"], st.session_state.structured_data["Skills"]["SOFT"]),
                "Repetition Checker": lambda: repetition("\n".join(st.session_state.structured_data["Description"])),
                "Verb Tense Checker": lambda: verb_tense("\n".join(st.session_state.structured_data["Description"])),
                "Responsibility In Words Checker": lambda: reponsibility("\n".join(st.session_state.structured_data["Description"])),
                "Spelling Checker": lambda: spelling_checker("\n".join(st.session_state.structured_data["Description"]))
            }

            pdf_list = [
                "Bullet Point Length", "Bullet Points Improver", "Quantification Checker",
                "Weak Verb Checker", "Repetition Checker", "Verb Tense Checker",
                "Responsibility In Words Checker", "Personal Info"
            ]

            show_dict = {
                "Resume Length": show_box_brevity,
                "Bullet Point Length": show_big_bullet_points,
                "Total Bullet Points": show_box_brevity,
                "Bullet Points Improver": show_bullet_point_improver,
                "Personal Info": show_personal_info,
                "Section Checker": show_personal_info,
                "Skill Checker": show_skill_checker,
                "Repetition Checker": show_repetition,
                "Weak Verb Checker": show_weak_verb,
                "Verb Tense Checker": show_verb_tense,
                "Responsibility In Words Checker": show_responsibility,
                "Spelling Checker": show_spell_checker
            }

            for analysis_name, analysis_function in analysis_functions.items():
                if st.sidebar.button(analysis_name):
                    if analysis_name not in st.session_state.analysis_results:
                        result = perform_analysis(analysis_name, analysis_function)
                        st.session_state.analysis_results[analysis_name] = result
                    else:
                        result = st.session_state.analysis_results[analysis_name]

                    if result:
                        if analysis_name in show_dict:
                            show_dict[analysis_name](result)
                        
                        if analysis_name not in pdf_list:
                            show_pdf_from_bytes(uploaded_file.getvalue())
                        
                        if analysis_name in pdf_list:
                            if analysis_name not in st.session_state.highlighted_pdfs:
                                highlighted_pdf_path = generate_highlighted_pdf(analysis_name, result, uploaded_file)
                                st.session_state.highlighted_pdfs[analysis_name] = highlighted_pdf_path.getvalue()

                            st.download_button(
                                label="Download Highlighted PDF",
                                data=st.session_state.highlighted_pdfs[analysis_name],
                                file_name=f"highlighted_{analysis_name}.pdf",
                                mime="application/pdf"
                            )
                            show_pdf_from_bytes(st.session_state.highlighted_pdfs[analysis_name])
                    else:
                        st.subheader("Everything Looks Pretty Good in This Section, Perfect!")
                        show_pdf_from_bytes(uploaded_file.getvalue())

def generate_highlighted_pdf(analysis_name, result, uploaded_file):
    if analysis_name == "Quantification Checker":
        return highlight_common(
            pdf_file=uploaded_file, color=colour_dict["green"],
            data=result["Quantify"], data2=result["Not Quantify"],
            color2=colour_dict["red"], two_sections=True
        )
    elif analysis_name == "Repetition Checker":
        exact_matches_list = [item for key, items in result.items() for item in items["text"]]
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["yellow"], data=exact_matches_list)
    elif analysis_name == "Bullet Points Improver":
        exact_matches_list = [item["original"] for key, items in result.items() for item in items]
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["blue"], data=exact_matches_list)
    elif analysis_name in ["Weak Verb Checker", "Verb Tense Checker", "Responsibility In Words Checker", "Personal Info"]:
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["yellow"], data=result.keys())
    elif analysis_name == "Bullet Point Length":
        return highlight_common(pdf_file=uploaded_file, color=colour_dict["red"], data=result["Result"])
    else:
        return uploaded_file

if __name__ == "__main__":
    main()