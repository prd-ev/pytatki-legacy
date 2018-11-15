import React from "react";
import style from "../scss/AddContent.scss";
import Modal from "./Modal.jsx";

const AddFile = props => {
  let uploadFile = e => {
    e.preventDefault();
    const form = document.getElementById("fileForm");
    const file = form[1].files[0];
    const title = form[0].value;
    var formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append(
      "notegroup_id",
      props.that.state.currentDirId[props.that.state.currentDepth]
    );
    fetch(props.that.state.siteUrl + "/add/", {
      method: "POST",
      body: formData
    })
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    props.that.updateContent();
    e.target.querySelector("input").value = null;
  };

  return (
    <div>
        <h5>Dodaj notatkę w aktualnym folderze</h5>
        <div>
          <form id="fileForm" className={style.form} onSubmit={uploadFile}>
            <label htmlFor="fileTitle">Tytuł notatki</label>
            <br />
            <input required type="text" name="title" id="fileTitle" />
            <br />
            <label htmlFor="noteFile">Plik notatki</label>
            <br />
            <input required className="btn" className={style.chooseFile} type="file" name="file" id="noteFile" />
            <br />
            <input type="submit" className="btn" value="Dodaj" />
          </form>
        </div>
    </div>
  );
};

export default React.memo(AddFile);
