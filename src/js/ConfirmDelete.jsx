import React from 'react';
import ComponentStyle from '../scss/ConfirmDelete.scss';

export default function ConfirmDelete(props) {
    let deleteNote = e => () => {
        let noteId = e;
        fetch(props.siteUrl + '/admin/delete/note/' + noteId, {
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
        props.updateContent();
    }

    let deleteFolder = e => () => {
        let folderId = e;
        fetch(props.siteUrl + '/notegroup/' + folderId + '/delete/', {
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
        props.updateContent();
    }

    if (props.noteToDelete) {
        return (
            <div className={ComponentStyle.deleteConfirmation}>
                <p>Jesteś pewien, że chcesz usunąć tą notatkę?</p>
                <span onClick={deleteNote(props.noteToDelete)}>Tak</span>
                <span onClick={() => props.that.setState({ noteToDelete: null })}>Nie</span>
            </div>
        )
    } else if (props.folderToDelete) {
        return (
            <div className={ComponentStyle.deleteConfirmation}>
                <p>Jesteś pewien, że chcesz usunąć ten folder?</p>
                <span onClick={deleteFolder(props.folderToDelete)}>Tak</span>
                <span onClick={() => props.that.setState({ folderToDelete: null })}>Nie</span>
            </div>
        )
    } else {
        return null;
    }

}
