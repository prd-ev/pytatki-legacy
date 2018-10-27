import React from "react";
import ComponentStyle from '../scss/AddContent.scss'

const AddNote = (props) => {
  return (
    <div>
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#addNote">Dodaj notatkę</button>
      <div class="modal" tabindex="-1" role="dialog" id="addNote">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Dodaj notatkę w aktualnym folderze</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form id="form" className={ComponentStyle.form} onSubmit={props.uploadNote}>
                <label for="noteTitle">Tytuł notatki</label>
                <br />
                <input required type="text" name="title" id="noteTitle"></input>
                <br />
                <label for="noteFile">Plik notatki</label>
                <br />
                <input required id="file" type="file" name="file" id="noteFile"></input>
                <br />
                <input type="submit" value="Dodaj"></input>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
};


export default AddNote;
