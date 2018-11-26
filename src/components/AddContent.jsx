import React from "react";
import AddFolder from "./AddFolder.jsx";
import AddFile from "./AddFile.jsx";
import AddNote from "./AddNote.jsx";
import Modal from "./Modal.jsx";
import style from "../scss/AddContent.scss";

function AddContent(props) {
  return (
    <div>
      <Modal name="+">
        <div className={style.addContainer}>
          <AddFile that={props.that} />
          <AddFolder that={props.that} />
          <AddNote that={props.that} />
        </div>
      </Modal>
    </div>
  );
}

export default React.memo(AddContent);
