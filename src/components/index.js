import Notatki from "./Notatki.jsx";
import React from "react";
import ReactDOM from "react-dom";

ReactDOM.render(<Notatki />, document.getElementById("reactEntry"));

let element = document.getElementById("reactEntry");
let fragment = document.createDocumentFragment();
while (element.firstChild) {
    fragment.appendChild(element.firstChild);
}
element.parentNode.replaceChild(fragment, element);
