import React from "react";
import style from "../scss/AddContent.scss";

const AddFolder = props => {
  let addFolder = e => {
    e.preventDefault();
    fetch(
      props.that.state.siteUrl +
        `/api/?query=mutation{createNotegroup(name:"${
          document.getElementById("addFolderForm")[0].value
        }", id_usergroup: ${props.that.state.currentUsergroupId}, parent_id: ${
          props.that.state.currentDirId[props.that.state.currentDepth]
        }, access_token: "${props.that.state.token}")}`,
      {
        method: "POST"
      }
    )
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => success.data.createNotegroup // Handle the success response object
      )
      .then(s => JSON.parse(s))
      .then(json =>
        typeof json.data === "string" || json.data instanceof String
          ? alert(json.data)
          : alert("dodano folder")
      )
      .catch(
        error => console.error(error) // Handle the error response object
      )
      .then(r => props.that.updateContent());
    e.target.querySelector("input").value = null;
  };

  return (
    <div>
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
    </div>
  );
};

export default React.memo(AddFolder);
