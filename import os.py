import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="AI Study Material Generator",
    page_icon="📚",
    layout="wide"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_study_material(topic, level, exam_type, days, material_type, extra_instructions):
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    prompt = f"""
You are an expert teacher and study coach.

Create study material for the following request.

Topic:
{topic}

Student level:
{level}

Exam or purpose:
{exam_type}

Available study time:
{days} days

Material type:
{material_type}

Extra instructions:
{extra_instructions or "None"}

Return the answer in clean Markdown.

Include these sections when useful:
1. Overview
2. Key Concepts
3. Detailed Notes
4. Important Formulas / Definitions
5. Examples
6. Flashcards
7. Practice Questions
8. Quiz With Answers
9. Study Plan
10. Revision Checklist

Make the content clear, exam-focused, and easy to revise.
"""

    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0.4,
    )

    return response.output_text


def save_markdown(content, topic):
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_topic = safe_topic.replace(" ", "_") or "study_material"
    filename = f"{safe_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    return filename, content.encode("utf-8")


st.title("AI Study Material Generator")

with st.sidebar:
    st.header("Settings")

    level = st.selectbox(
        "Student level",
        ["School", "High School", "College", "University", "Beginner", "Intermediate", "Advanced"]
    )

    exam_type = st.text_input(
        "Exam / purpose",
        placeholder="Example: board exam, semester exam, interview, revision"
    )

    days = st.number_input(
        "Study time in days",
        min_value=1,
        max_value=365,
        value=7
    )

    material_type = st.multiselect(
        "Generate",
        [
            "Summary",
            "Detailed Notes",
            "Flashcards",
            "Quiz",
            "Practice Questions",
            "Study Plan",
            "Revision Checklist"
        ],
        default=["Detailed Notes", "Flashcards", "Quiz", "Study Plan"]
    )

topic = st.text_area(
    "Enter topic or syllabus",
    height=180,
    placeholder="Example: Photosynthesis, Newton's Laws, DBMS normalization, Indian Constitution..."
)

extra_instructions = st.text_area(
    "Extra instructions",
    height=100,
    placeholder="Example: Make it simple, include diagrams in text, focus on MCQs, explain with examples..."
)

generate_button = st.button("Generate Study Material", type="primary")

if generate_button:
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Missing OPENAI_API_KEY. Add it to your .env file.")
    elif not topic.strip():
        st.warning("Please enter a topic or syllabus.")
    else:
        with st.spinner("Generating your study material..."):
            try:
                result = generate_study_material(
                    topic=topic,
                    level=level,
                    exam_type=exam_type,
                    days=days,
                    material_type=", ".join(material_type),
                    extra_instructions=extra_instructions
                )

                st.success("Study material generated!")

                tab1, tab2 = st.tabs(["Preview", "Download"])

                with tab1:
                    st.markdown(result)

                with tab2:
                    filename, file_data = save_markdown(result, topic)
                    st.download_button(
                        label="Download Markdown File",
                        data=file_data,
                        file_name=filename,
                        mime="text/markdown"
                    )

            except Exception as error:
                st.error(f"Something went wrong: {error}")