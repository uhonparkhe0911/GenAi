# action_items_provider_app.py

import os
import json
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="Meeting Action Items Extractor",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Meeting Action Items Extractor")
st.write("Upload a meeting transcript to extract action items and their owners.")

# Define the structure of each action item
class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task: str
    owner: str


# Define the overall output structure
class Summary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_owner_list: list[ActionItem]


# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please configure it in your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Upload meeting transcript
uploaded_file = st.file_uploader(
    "Upload meeting transcript",
    type=["txt"]
)

if uploaded_file is not None:
    document = uploaded_file.read().decode("utf-8")

    with st.expander("View meeting transcript"):
        st.text(document)

    if st.button("Extract Action Items", type="primary"):
        prompt = f"""
Read the following meeting transcript and extract all action items.

For every action item, identify:
- task: What needs to be done, including the deadline if specified.
- owner: The person responsible for completing the task.

If the owner is not explicitly identified, use "Unassigned".
Do not invent task assignments.

Meeting transcript:
{document}
"""

        try:
            with st.spinner("Extracting action items..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "action_items_summary",
                            "strict": True,
                            "schema": Summary.model_json_schema()
                        }
                    }
                )

                action_items = Summary.model_validate_json(
                    response.choices[0].message.content
                )

            st.success(
                f"Successfully extracted {len(action_items.task_owner_list)} action items!"
            )

            # Display action items
            st.subheader("Extracted Action Items")

            for index, item in enumerate(
                action_items.task_owner_list, start=1
            ):
                with st.container(border=True):
                    st.markdown(f"**Task {index}**")
                    st.write(item.task)
                    st.markdown(f"**Owner:** {item.owner}")

            # Generate JSON output
            json_output = json.dumps(
                action_items.model_dump(),
                indent=2,
                ensure_ascii=False
            )

            st.subheader("Structured JSON Output")
            st.code(json_output, language="json")

            # Download JSON file
            st.download_button(
                label="Download Action Items as JSON",
                data=json_output,
                file_name="action_items.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")