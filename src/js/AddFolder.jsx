import React, { Component } from 'react';
import ComponentStyle from '../scss/AddContent.scss';

export default class AddFolder extends Component {
  constructor(props) {
    super(props)
  }

  render() {
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
                <form id="addFolderForm" className={ComponentStyle.form} onSubmit={this.props.addFolder}>
                  <label htmlFor="folderTitle">Tytuł folderu</label>
                  <br />
                  <input required name="title" type="text" id="folderTitle"/>
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
    )
  }
}
