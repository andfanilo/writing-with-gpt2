import { Quill } from "react-quill"

const Inline = Quill.import("blots/inline");

class CustomMentionBlot extends Inline {
    static create(data) {
        const node = super.create();
        node.innerHTML = data.value;
        return node;
    }
}

CustomMentionBlot.blotName = "custom_mention";
CustomMentionBlot.tagName = "span";
CustomMentionBlot.className = "mention";

export default CustomMentionBlot;
