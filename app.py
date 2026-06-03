import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="AI Study Material Generator (Offline)",
    page_icon="📚",
    layout="wide"
)


def generate_study_material(topic, level, exam_type, days, extra_instructions):
    exam_text = exam_type.strip() if exam_type.strip() else "general learning"

    content = f"""
# 📚 Study Material: {topic}

## 🎯 Overview
This study material is designed for **{level}** level students preparing for **{exam_text}**.

You have **{days} day(s)** to study this topic effectively.

---

## 📌 Key Concepts
- Basic understanding of {topic}
- Core principles and definitions
- Important facts, formulas, or ideas
- Common mistakes to avoid

---

## 🧠 Detailed Notes
The topic **{topic}** should be studied step by step.

Focus on:
- Understanding the meaning of important terms
- Learning definitions clearly
- Connecting concepts with examples
- Practicing questions regularly
- Revising important points before the exam

---

## 📖 Important Definitions
- Definition 1 related to {topic}
- Definition 2 related to {topic}
- Definition 3 related to {topic}

---

## 💡 Examples
Example 1: Real-world application of {topic}

Example 2: Problem-solving example related to {topic}

Example 3: Short exam-style example

---

## 🧪 Practice Questions
1. What is {topic}?
2. Explain the key concepts of {topic}.
3. Write short notes on {topic}.
4. Give examples related to {topic}.
5. Why is {topic} important?

---

## 🧾 Quiz: Self Test
1. Define {topic}.
2. List three important points about {topic}.
3. Give one example of {topic}.
4. Explain how {topic} is used in real life.
5. Write a short summary of {topic}.

---

## 📅 Study Plan: {days} Day(s)

"""

    for day in range(1, days + 1):
        if day == 1:
            content += f"- Day {day}: Understand the basics of {topic}\n"
        elif day == days:
            content += f"- Day {day}: Final revision and self-test\n"
        else:
            content += f"- Day {day}: Study subtopics, examples, and practice questions\n"

    content += f"""

---

## ✅ Revision Checklist
- [ ] Understand the basics of {topic}
- [ ] Learn important definitions
- [ ] Review examples
- [ ] Solve practice questions
- [ ] Take the self-test
- [ ] Revise weak areas

---

## 📝 Extra Instructions
{extra_instructions.strip() if extra_instructions.strip() else "No extra instructions provided."}

---

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    return content


def save_markdown(content, topic):
    safe_topic = "".join(
        c for c in topic if c.isalnum() or c in (" ", "-", "_")
    ).strip()

    safe_topic = safe_topic.replace(" ", "_") or "study_material"

    filename = f"{safe_topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    return filename, content.encode("utf-8")


st.title("📚 AI Study Material Generator")
st.caption("Offline version - no API key required")

level = st.selectbox(
    "Student level",
    [
        "School",
        "High School",
        "College",
        "University",
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

exam_type = st.text_input("Exam / purpose", placeholder="Example: Board exam, NEET, JEE, UPSC")

days = st.number_input(
    "Study time in days",
    min_value=1,
    max_value=365,
    value=7,
    step=1
)

topic = st.text_area(
    "Enter topic or syllabus",
    placeholder="Example: Photosynthesis, Python basics, Indian Constitution"
)

extra_instructions = st.text_area(
    "Extra instructions",
    placeholder="Example: Include simple examples and short questions"
)

generate_button = st.button("Generate Study Material", type="primary")

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        result = generate_study_material(
            topic=topic.strip(),
            level=level,
            exam_type=exam_type,
            days=int(days),
            extra_instructions=extra_instructions
        )

        st.success("Study material generated successfully!")

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