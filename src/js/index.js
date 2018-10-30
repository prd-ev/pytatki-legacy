import Notatki from "./Notatki.jsx";
import React from "react";
import ReactDOM from "react-dom";
import ComponentStyle from "../scss/global.scss"

ReactDOM.render(<Notatki/>, document.getElementById("reactEntry"));

var element = document.getElementById("reactEntry");
var fragment = document.createDocumentFragment();
while(element.firstChild) {
    fragment.appendChild(element.firstChild);
}
element.parentNode.replaceChild(fragment, element);
