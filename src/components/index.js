import Notatki from "./Notatki.jsx";
import React from "react";
import ReactDOM from "react-dom";
import style from "../scss/global.scss";

ReactDOM.render(<Notatki />, document.getElementById("reactEntry"));

let element = document.getElementById("reactEntry");
let fragment = document.createDocumentFragment();
while (element.firstChild) {
  fragment.appendChild(element.firstChild);
}
element.parentNode.replaceChild(fragment, element);

let sidebar = document.getElementById("sidebar");
let nav = document.querySelector("nav");

let openSwipeArea = document.getElementById("openSwipeArea");
let openHammer = new Hammer(openSwipeArea);
openHammer.on("swiperight", () => {
  if (!sidebar.classList.contains("navOpen")) {
    sidebar.animate([{ left: "-70vw" }, { left: "0" }], { duration: 300 });
    nav.animate([{ left: "-70vw" }, { left: "0" }], { duration: 300 });
    sidebar.classList.add("navOpen");
    nav.classList.add("navOpen");
  }
});

let closeSwipeArea = document.getElementById("closeSwipeArea");
let closeHammer = new Hammer(closeSwipeArea);
closeHammer.on("swipeleft tap", () => {
  if (sidebar.classList.contains("navOpen")) {
    sidebar.animate([{ left: "0" }, { left: "-70vw" }], { duration: 300 });
    nav.animate([{ left: "0" }, { left: "-70vw" }], { duration: 300 });
    sidebar.classList.remove("navOpen");
    nav.classList.remove("navOpen");
  }
});
