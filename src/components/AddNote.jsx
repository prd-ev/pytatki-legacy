import React from "react";
import style from "../scss/AddContent.scss";

const AddNote = props => {
  const createNote = e => {
    e.preventDefault();
    const title = document.getElementById("noteTitle").value;
    const formData = new FormData();
    formData.append(
      "notegroup_id",
      props.that.state.currentDirId[props.that.state.currentDepth]
    );
    formData.append("title", title);
    fetch(props.that.state.siteUrl + "/add_note/", {
      method: "POST",
      body: formData
    })
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => {
          alert(success.data);
          if (success.data.includes("zostala dodana")) {
            window.open("/deaditor/" + success.data.match(/\d+/g));
          }
        } // Handle the success response object
      )
      .then(r => props.that.updateContent())
      .catch(
        error => console.error(error) // Handle the error response object
      );
    e.target.querySelector("input").value = null;
  };

  return (
    <div>
      <h5>Stwórz nową notatkę w aktualnym folderze</h5>
      <div>
        <form id="form" className={style.form} onSubmit={createNote}>
          <label htmlFor="noteTitle">Tytuł notatki</label>
          <br />
          <input required type="text" name="title" id="noteTitle" />
          <br />
          <input type="submit" className="btn" value="Dodaj" />
        </form>
      </div>
    </div>
  );
};

export default React.memo(AddNote);
