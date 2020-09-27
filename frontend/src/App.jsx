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
  const [editorContent, setEditorContent] = useState(
    store.get("editorContent", "")
  ) // HTML content of editor, optimized and usable by Quill
  const reactQuillRef = useRef() // Ref access to editor

  const handleLoadingMentionEvent = useCallback(() => {
    return "Loading..."
  }, [])

  const handleFetchMentionEvent = useCallback(
    async (searchTerm, renderItem) => {
      const editorContentAsText = reactQuillRef.current.getEditor().getText()
      // TODO: API error handling
      const response = await axios.post("http://localhost:8000/api/suggest", {
        text: editorContentAsText,
      })
      const suggestions = response["data"]
      renderItem(suggestions, searchTerm)
    },
    []
  )

  const handleEditorContentEdit = useCallback((content) => {
    store.set("editorContent", content)
    setEditorContent(content)
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
        value={editorContent}
        onChange={handleEditorContentEdit}
      />
      <button style={{ marginTop: "1em" }} onClick={() => setEditorContent("")}>
        Clear editor
      </button>
    </div>
  )
}

export default App
