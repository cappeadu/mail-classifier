import os

import pandas as pd
import streamlit as st

INPUT_FILE = "data/emails.csv"
OUTPUT_FILE = "data/annotated_emails.csv"

CATEGORIES = [
    "social_media",
    "work",
    "jobs",
    "finance",
    "shopping",
    "personal",
    "transportation",
    "education",
    "notifications",
]


def load_data():
    """Load the original emails and create the annotation file if needed."""

    emails = pd.read_csv(INPUT_FILE)

    if os.path.exists(OUTPUT_FILE):
        annotated = pd.read_csv(OUTPUT_FILE)
    else:
        annotated = emails.copy()
        annotated["label"] = ""

    return annotated


def save_data(df):
    """Save annotations to the separate annotation file."""
    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )


st.set_page_config(
    page_title="Gmail Email Annotation",
    layout="wide",
)

st.title("Gmail Email Annotation")

df = load_data()

# Make sure label column exists.
if "label" not in df.columns:
    df["label"] = ""

# Find unannotated emails.
unannotated = df[df["label"].isna() | (df["label"].astype(str).str.strip() == "")]

annotated_count = len(df) - len(unannotated)
total_count = len(df)

st.progress(annotated_count / total_count if total_count > 0 else 0)

st.write(f"Annotated: **{annotated_count} / {total_count}**")

if len(unannotated) == 0:
    st.success("All emails have been annotated!")
    st.stop()

# Always work on the first unannotated email.
email_index = unannotated.index[0]
email = df.loc[email_index]

st.divider()

st.subheader(f"Email {annotated_count + 1} of {total_count}")

st.write("**From:**", email["sender"])
st.write("**Subject:**", email["subject"])
st.write("**Date:**", email["date"])

st.divider()

st.subheader("Email body")

body = email["body"]

if pd.isna(body):
    body = "[No email body available]"

st.text_area(
    "Body",
    str(body),
    height=400,
    disabled=True,
)

st.divider()

st.subheader("Choose a category")

label = st.radio(
    "Category",
    CATEGORIES,
)

if st.button(
    "Save annotation",
    type="primary",
):
    df.at[email_index, "label"] = label

    save_data(df)

    st.success(f"Saved as '{label}'.")

    st.rerun()
