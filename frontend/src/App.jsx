import React, { useCallback, useRef, useState } from "react"
import ReactQuill, { Quill } from "react-quill"

import axios from "axios"
import store from "store"
import "quill-mention"
import "quill-mention/dist/quill.mention.css"

import "./App.css"

// Use a customized render of suggestions in text editor
import CustomMentionBlot from "./blots/CustomMentionBlot"
Quill.register(CustomMentionBlot)

const App = () => {
  const [value, setValue] = useState(store.get("editorContent", "")) // HTML Quill-optimized
  const reactQuillRef = useRef() // get access to editor

  const handleLoadingMentionEvent = useCallback(() => {
    return "Loading..."
  }, [])

  const handleFetchMentionEvent = useCallback(
    async (searchTerm, renderItem) => {
      const editorContents = reactQuillRef.current.getEditor().getText()
      // TODO: API error handling
      const response = await axios.post("http://localhost:8000/api/suggest", {
        text: editorContents,
      })
      const suggestions = response["data"]

      renderItem(suggestions, searchTerm)
    },
    []
  )

  const handleValueEdit = useCallback((content) => {
    store.set("editorContent", content)
    setValue(content)
  }, [])

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
      <h1>Write with Transformer demo</h1>
      <ReactQuill
        ref={reactQuillRef}
        theme="snow"
        placeholder="Enter something..."
        modules={modules}
        formats={formats}
        value={value}
        onChange={handleValueEdit}
      />
      <button style={{ marginTop: "1em" }} onClick={() => setValue("")}>
        Clear editor
      </button>
    </div>
  )
}

export default App
