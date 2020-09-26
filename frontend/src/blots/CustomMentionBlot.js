import { Quill } from "react-quill"

const Embed = Quill.import("blots/embed");

class CustomMentionBlot extends Embed {
    static create(data) {
        const node = super.create();
        const denotationChar = document.createElement("span");
        denotationChar.className = "ql-mention-denotation-char";
        denotationChar.innerHTML = data.value;
        denotationChar.setAttribute('contenteditable', true);
        node.appendChild(denotationChar);
        return CustomMentionBlot.setDataValues(node, data);
    }

    static setDataValues(element, data) {
        const domNode = element;
        Object.keys(data).forEach(key => {
            domNode.dataset[key] = data[key];
        });
        return domNode;
    }

    static value(domNode) {
        return domNode.dataset;
    }
}

CustomMentionBlot.blotName = "custom_mention";
CustomMentionBlot.tagName = "span";
CustomMentionBlot.className = "mention";

export default CustomMentionBlot;
