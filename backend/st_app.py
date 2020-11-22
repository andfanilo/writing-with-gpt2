import streamlit as st

from aitextgen import aitextgen


@st.cache(allow_output_mutation=True, ttl=600, max_entries=3)
def load_aitextgen(model: str):
    return aitextgen(model=model)


def generate_text(ai, prefix, nsamples, length_gen, temperature, topk, topp):
    return ai.generate(
        n=nsamples,
        batch_size=nsamples,
        prompt=prefix,
        max_length=length_gen,
        temperature=temperature,
        top_k=topk,
        top_p=topp,
        return_as_list=True,
    )


def main():
    st.title("Debugging aitextgen")
    st.sidebar.subheader("Configuration")

    selected_model = st.sidebar.selectbox("Choose a model: ", ("distilgpt2", "gpt2"))
    ai = load_aitextgen(selected_model)

    nsamples = st.sidebar.number_input("Num samples: ", 1, 10, 3)
    length_gen = st.sidebar.select_slider(
        "Length generated elements: ", [r * 10 for r in range(1, 11)], 50
    )
    temperature = st.sidebar.slider("Choose temperature: ", 0.0, 1.0, 0.9, 0.1)
    topk = st.sidebar.slider("Choose topk: ", 0, 5, 0)
    topp = st.sidebar.slider("Choose topp: ", 0.0, 1.0, 0.9, 0.1)

    prefix = st.text_area("Enter text: ")
    generated = generate_text(ai, prefix, nsamples, length_gen, temperature, topk, topp)

    st.header("Generation")
    for gen in generated:
        st.markdown(f"{gen}\n<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
