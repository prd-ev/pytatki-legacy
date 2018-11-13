import React from "react";
import style from "../scss/AddContent.scss";
import Modal from "./Modal.jsx";

const AddFolder = props => {
  let addFolder = e => {
    e.preventDefault();
    var formData = new FormData();
    formData.append("title", document.getElementById("addFolderForm")[0].value);
    formData.append(
      "parent_id",
      props.that.state.currentDirId[props.that.state.currentDepth]
    );
    formData.append("class", "1"); //dodać dynamicznie
    fetch(props.that.state.siteUrl + "/admin/add/", {
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
      <Modal name="Dodaj folder">
        <div>
          <h5>Dodaj folder w aktualnej lokalizacji</h5>
        </div>
        <div>
          <form id="addFolderForm" className={style.form} onSubmit={addFolder}>
            <label htmlFor="folderTitle">Tytuł folderu</label>
            <br />
            <input required name="title" type="text" id="folderTitle" />
            <br />
            <input className="btn" type="submit" value="Dodaj" />
          </form>
        </div>
      </Modal>
    </div>
  );
};

export default React.memo(AddFolder);
