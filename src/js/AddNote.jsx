import React from "react";
import ComponentStyle from '../scss/AddContent.scss';

const AddNote = (props) => {
  return (
    <div>
      <button type="button" className="btn" data-toggle="modal" data-target="#addNote">Dodaj notatkę</button>
      <div className="modal" tabIndex="-1" role="dialog" id="addNote">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Dodaj notatkę w aktualnym folderze</h5>
              <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <form id="form" className={ComponentStyle.form} onSubmit={props.uploadNote}>
                <label htmlFor="noteTitle">Tytuł notatki</label>
                <br />
                <input required type="text" name="title" id="noteTitle"></input>
                <br />
                <label htmlFor="noteFile">Plik notatki</label>
                <br />
                <input required id="file" type="file" name="file" id="noteFile"></input>
                <br />
                <input type="submit" value="Dodaj"></input>
              </form>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
};


export default AddNote;
