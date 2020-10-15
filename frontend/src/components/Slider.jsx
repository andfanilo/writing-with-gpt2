import React from "react"

const Slider = ({ label, name, min, max, step, state, dispatch }) => {
  return (
    <label style={{ marginRight: "1em" }}>
      {label}
      <input
        name={name}
        type="number"
        min={min}
        max={max}
        step={step}
        value={state}
        onChange={dispatch}
      ></input>
    </label>
  )
}

export default Slider
