import React, { useState } from "react"
import ReactQuill from "react-quill"
import axios from "axios"
import "quill-mention"
import "quill-mention/dist/quill.mention.css"
import "./App.css"

const mentionFunc = async (searchTerm, renderItem, mentionChar) => {
  let values
  if (mentionChar === "@" || mentionChar === "#") {
    const response = await axios.post("http://localhost:8000/api/generate", {
      text: "Hello world",
    })
    values = response["data"]
  } else {
    alert("HTTP-Error")
  }
  if (searchTerm.length === 0) {
    renderItem(values, searchTerm)
  } else {
    const matches = []
    for (let i = 0; i < values.length; i++)
      if (~values[i].value.toLowerCase().indexOf(searchTerm.toLowerCase()))
        matches.push(values[i])
    renderItem(matches, searchTerm)
  }
}

const App = () => {
  const [value, setValue] = useState("")

  const modules = {
    toolbar: [
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
    ],
    mention: {
      allowedChars: /^[A-Za-z\s]*$/,
      mentionDenotationChars: ["@", "#"],
      source: mentionFunc,
    },
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
    "mention",
  ]

  return (
    <div>
      <h1>Write with Transformer demo</h1>
      <ReactQuill
        theme="snow"
        placeholder="Enter something..."
        modules={modules}
        formats={formats}
        value={value}
        onChange={setValue}
      />
    </div>
  )
}

export default App
