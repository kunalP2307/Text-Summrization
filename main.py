import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import streamlit as st

text = ""

if not hasattr(st.session_state, "output"):
    st.session_state.output = ""

def get_summary():
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    st.session_state.output = summary
    show_summary()

def show_summary():
    st.title("Summary")
    st.markdown(st.session_state.output , unsafe_allow_html=True)

if __name__ == "__main__":
    # st.set_page_config(page_title="Enter Text")
    st.title("Text Summarization")
    text = st.text_area(label= "Enter Text")

    st.button(label= "Get Summary", on_click= get_summary)

