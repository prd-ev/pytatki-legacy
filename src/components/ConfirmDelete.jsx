import React from 'react';
import style from '../scss/ConfirmDelete.scss';

export default function ConfirmDelete(props) {
    let deleteNote = noteId => () => {
        fetch(props.that.state.siteUrl + '/admin/delete/note/' + noteId, {
        }).then(
            response => response.json() // if the response is a JSON object
        ).then(
            success => alert(success.data) // Handle the success response object
        ).catch(
            error => console.log(error) // Handle the error response object
        );
        props.that.setState({
            noteToDelete: null
        })
        props.that.updateContent();
    }

    let deleteFolder = folderId => () => {
        fetch(props.that.state.siteUrl + '/notegroup/' + folderId + '/delete/', {
        }).then(
            response => response.json() // if the response is a JSON object
        ).then(
            success => alert(success.data) // Handle the success response object
        ).catch(
            error => console.log(error) // Handle the error response object
        );
        props.that.setState({
            folderToDelete: null
        })
        props.that.updateContent();
    }

    if (props.that.state.noteToDelete) {
        return (
            <div className={style.deleteConfirmation}>
                <p>Jesteś pewien, że chcesz usunąć tą notatkę?</p>
                <span onClick={deleteNote(props.that.state.noteToDelete)}>Tak</span>
                <span onClick={() => props.that.setState({ noteToDelete: null })}>Nie</span>
            </div>
        )
    } else if (props.that.state.folderToDelete) {
        return (
            <div className={style.deleteConfirmation}>
                <p>Jesteś pewien, że chcesz usunąć ten folder?</p>
                <span onClick={deleteFolder(props.that.state.folderToDelete)}>Tak</span>
                <span onClick={() => props.that.setState({ folderToDelete: null })}>Nie</span>
            </div>
        )
    } else {
        return null;
    }
}
