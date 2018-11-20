import React from "react";
import style from "../scss/ConfirmDelete.scss";
import Modal from "./Modal.jsx";

export default function ConfirmDelete(props) {
  let deleteNote = noteId => () => {
    fetch(props.that.state.siteUrl + "/admin/delete/note/" + noteId, {})
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.error(error) // Handle the error response object
      );
    props.that.updateContent();
    props.that.setState({
      noteToDelete: null
    });
  };

  let deleteFolder = folderId => () => {
    fetch(props.that.state.siteUrl + "/notegroup/" + folderId + "/delete/", {})
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.error(error) // Handle the error response object
      );
    props.that.updateContent();
    props.that.setState({
      folderToDelete: null
    });
  };

  const isMobile = window.innerWidth <= 500;

  if (props.that.state.noteToDelete) {
    if (isMobile) {
      return (
        <Modal
          no_button={true}
          close_action={() => props.that.setState({ noteToDelete: null })}
        >
          <p>Jesteś pewien, że chcesz usunąć tą notatkę?</p>
          <button
            className="btn"
            style={{ margin: "10px" }}
            onClick={deleteNote(props.that.state.noteToDelete)}
          >
            Tak
          </button>
          <button
            className="btn"
            style={{ margin: "10px" }}
            onClick={() => props.that.setState({ noteToDelete: null })}
          >
            Nie
          </button>
        </Modal>
      );
    } else {
      return (
        <div className={style.deleteConfirmation}>
          <p>Jesteś pewien, że chcesz usunąć tą notatkę?</p>
          <span onClick={deleteNote(props.that.state.noteToDelete)}>Tak</span>
          <span onClick={() => props.that.setState({ noteToDelete: null })}>
            Nie
          </span>
        </div>
      );
    }
  } else if (props.that.state.folderToDelete) {
    if (isMobile) {
      return (
        <Modal
          no_button={true}
          close_action={() => props.that.setState({ folderToDelete: null })}
        >
          <p>Jesteś pewien, że chcesz usunąć ten folder?</p>

          <button
            className="btn"
            style={{ margin: "10px" }}
            onClick={deleteFolder(props.that.state.folderToDelete)}
          >
            Tak
          </button>
          <button
            className="btn"
            style={{ margin: "10px" }}
            onClick={() => props.that.setState({ folderToDelete: null })}
          >
            Nie
          </button>
        </Modal>
      );
    } else {
      return (
        <div className={style.deleteConfirmation}>
          <p>Jesteś pewien, że chcesz usunąć ten folder?</p>
          <span onClick={deleteFolder(props.that.state.folderToDelete)}>
            Tak
          </span>
          <span onClick={() => props.that.setState({ folderToDelete: null })}>
            Nie
          </span>
        </div>
      );
    }
  } else {
    return null;
  }
}
