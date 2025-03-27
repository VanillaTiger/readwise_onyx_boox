import os

import streamlit as st
from src.notion import notion_processing
from src.thought_processing.files_processing import load_new_book_annotation
from src.thought_processing.files_processing import prepare_file_and_headers
from src.thought_processing.files_processing import save_thought_to_csv
from src.thought_processing.wise_thought import WiseThought


def main(filepath, output_path, author, title, pipeline=False):
    annotation_text = load_new_book_annotation(filepath)
    prepare_file_and_headers(output_path)

    data_splited = annotation_text.split("-------------------")
    st.write(f"Found {len(data_splited)-1} thoughts in the annotation")

    book_thoughts = []
    for item in data_splited:
        if item == "" or item == "\n":
            st.info("Found an empty line. End of file.")
            break
        try:
            thought = WiseThought(title=title, author=author, text=item)
            thought.extract_information()
            thought_to_save = thought.model_dump(
                include={
                    "highlight",
                    "title",
                    "author",
                    "url",
                    "note",
                    "location",
                    "date",
                }
            )
            book_thoughts.append(thought_to_save)
            save_thought_to_csv(thought_to_save, output_path)
        except AttributeError as e:
            st.warning(f"Could not parse the following thought: {item} error {e}")

    st.info("Finished parsing the annotation")
    if pipeline:
        st.info("Starting pipeline to send data to notion database")
        notion_processing.send_thoughts_to_database(book_thoughts)
        st.info("Data uploaded to notion database")
        notion_database = os.getenv("notion_DATABASE_ID")
        notion_USERNAME = os.getenv("notion_USERNAME")
        notion_url = f"https://notion.so/{notion_database}/{notion_USERNAME}"
        st.markdown(f"[Open Notion Database]({notion_url})", unsafe_allow_html=True)
    else:
        st.info("Notion pipeline not started")
        st.info(
            "Run notion_integration/notion_processing.py manually to send to notion database"
        )


st.title("Annotation Processor")
uploaded_file = st.file_uploader("Upload your annotation file", type=["txt"])
author = st.text_input("Author")
title = st.text_input("Title")
output_path = st.text_input(
    "Output Path", value=os.path.join("data_output", "output_streamlit.csv")
)
pipeline = st.checkbox("Send to Notion Database")

if st.button("Upload"):
    if uploaded_file is not None and author and title and output_path:
        with open("temp_annotation.txt", "wb") as f:
            f.write(uploaded_file.getbuffer())
        main("temp_annotation.txt", output_path, author, title, pipeline)
        os.remove("temp_annotation.txt")
    else:
        st.error("Please provide all inputs before uploading.")
