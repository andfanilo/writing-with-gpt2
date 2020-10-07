import React, { useCallback, useRef, useState } from "react"
import ReactQuill, { Quill } from "react-quill"
import "react-quill/dist/quill.snow.css"
import "quill-mention"
import "quill-mention/dist/quill.mention.css"

import axios from "axios"
import store from "store"

import "./App.css"

// Use a customized render of suggestions in text editor
import CustomMentionBlot from "./blots/CustomMentionBlot"
Quill.register(CustomMentionBlot)

const App = () => {
  const [editorContent, setEditorContent] = useState(
    store.get("editorContent", "")
  ) // HTML content of editor, optimized and usable by Quill
  const reactQuillRef = useRef() // Ref access to editor

  const [requestConfig, setRequestConfig] = useState({
    numSamples: 5,
    lengthSample: 10,
    lengthPrefix: 500,
  })

  const handleLoadingMentionEvent = useCallback(() => {
    return "Loading..."
  }, [])

  const handleFetchMentionEvent = useCallback(
    async (searchTerm, renderItem) => {
      const editorContentAsText = reactQuillRef.current.getEditor().getText()
      axios
        .post("/api/suggest", {
          text: editorContentAsText,
          nsamples: requestConfig.numSamples,
          length: requestConfig.lengthSample,
          lengthprefix: requestConfig.lengthPrefix,
        })
        .then((response) => {
          const suggestions = response["data"]
          renderItem(suggestions, searchTerm)
        })
        .catch((err) => alert(err))
    },
    [requestConfig]
  )

  const handleEditorContentEdit = useCallback((content) => {
    store.set("editorContent", content)
    setEditorContent(content)
  }, [])

  const handleInputChange = (event) => {
    setRequestConfig({
      ...requestConfig,
      [event.target.name]: event.target.value,
    })
  }

  const toolbarConfig = [
    [{ header: [1, 2, false] }],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [
      { list: "ordered" },
      { list: "bullet" },
      { indent: "-1" },
      { indent: "+1" },
    ],
    ["link", "image"],
    ["clean"],
  ]

  const mentionConfig = {
    allowedChars: /^[A-Za-z\s]*$/,
    mentionDenotationChars: ["@"],
    blotName: "custom_mention",
    fixMentionsToQuill: true,
    renderLoading: handleLoadingMentionEvent,
    source: handleFetchMentionEvent,
  }

  const modules = {
    toolbar: toolbarConfig,
    mention: mentionConfig,
  }

  const formats = [
    "header",
    "bold",
    "italic",
    "underline",
    "strike",
    "blockquote",
    "list",
    "bullet",
    "indent",
    "link",
    "image",
    "custom_mention",
  ]

  return (
    <div>
      <header className="header">
        <h1>GPT-2 editor</h1>
      </header>
      <section className="container">
        <ReactQuill
          ref={reactQuillRef}
          theme="snow"
          placeholder="Enter something..."
          modules={modules}
          formats={formats}
          value={editorContent}
          onChange={handleEditorContentEdit}
        />
      </section>
      <aside className="sidebar">
        <div>
          <label style={{ marginRight: "1em" }}>
            Number samples:
            <input
              name="numSamples"
              type="number"
              min="3"
              max="50"
              value={requestConfig.numSamples}
              onChange={handleInputChange}
            ></input>
          </label>
          <label style={{ marginRight: "1em" }}>
            Length samples:
            <input
              name="lengthSample"
              type="number"
              min="5"
              max="500"
              value={requestConfig.lengthSample}
              onChange={handleInputChange}
            ></input>
          </label>
          <label style={{ marginRight: "1em" }}>
            Length prefix:
            <input
              name="lengthPrefix"
              type="number"
              min="50"
              max="5000"
              value={requestConfig.lengthPrefix}
              onChange={handleInputChange}
            ></input>
          </label>
        </div>
        <button
          style={{ marginTop: "1em" }}
          onClick={() => setEditorContent("")}
        >
          Clear editor
        </button>
      </aside>
    </div>
  )
}

export default App
