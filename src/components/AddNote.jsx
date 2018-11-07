import React from "react";
import ComponentStyle from "../scss/AddContent.scss";

const AddNote = props => {
  let uploadNote = e => {
    e.preventDefault();
    const form = document.getElementById("form");
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
      <button
        type="button"
        className="btn bar"
        data-toggle="modal"
        data-target="#addNote"
      >
        Dodaj notatkę
      </button>
      <div className="modal" tabIndex="-1" role="dialog" id="addNote">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">
                Dodaj notatkę w aktualnym folderze
              </h5>
              <button
                type="button"
                className="close"
                data-dismiss="modal"
                aria-label="Close"
              >
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <form
                id="form"
                className={ComponentStyle.form}
                onSubmit={uploadNote}
              >
                <label htmlFor="noteTitle">Tytuł notatki</label>
                <br />
                <input required type="text" name="title" id="noteTitle" />
                <br />
                <label htmlFor="noteFile">Plik notatki</label>
                <br />
                <input required type="file" name="file" id="noteFile" />
                <br />
                <input type="submit" value="Dodaj" />
              </form>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-dismiss="modal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddNote;
