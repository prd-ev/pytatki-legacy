import React, { Component } from 'react';
import ComponentStyle from '../scss/AddContent.scss';

const AddFolder = (props) => {

  let addFolder = (e) => {
    e.preventDefault();
    var formData = new FormData();
    formData.append('title', document.getElementById('addFolderForm')[0].value);
    formData.append('parent_id', props.that.state.currentDirId[props.that.state.currentDirId.length - 1]);
    formData.append('class', '1');//dodać dynamicznie 
    fetch(props.that.state.siteUrl + '/admin/add/', {
      method: 'POST',
      body: formData
    }).then(
      response => response.json() // if the response is a JSON object
    ).then(
      success => alert(success.data) // Handle the success response object
    ).catch(
      error => console.log(error) // Handle the error response object
    );
    props.that.updateContent();
    e.target.querySelector("input").value = null;
  }

  return (
    <div>
      <button type="button" className="btn" data-toggle="modal" data-target="#addFolder">Dodaj folder</button>
      <div className="modal" tabIndex="-1" role="dialog" id="addFolder">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Dodaj folder w aktualnej lokalizacji</h5>
              <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <form id="addFolderForm" className={ComponentStyle.form} onSubmit={addFolder}>
                <label htmlFor="folderTitle">Tytuł folderu</label>
                <br />
                <input required name="title" type="text" id="folderTitle" />
                <br />
                <input type="submit" value="Dodaj" />
              </form>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddFolder;

