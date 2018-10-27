import React, { Component } from 'react'
import ComponentStyle from '../scss/AddContent.scss'

export default class AddFolder extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#addFolder">Dodaj folder</button>
        <div class="modal" tabindex="-1" role="dialog" id="addFolder">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Dodaj folder w aktualnej lokalizacji</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <form id="addFolderForm" className={ComponentStyle.form} onSubmit={this.props.addFolder}>
                  <label for="folderTitle">Tytuł folderu</label>
                  <br />
                  <input required name="title" type="text" id="folderTitle"/>
                  <br />
                  <input type="submit" value="Dodaj" />
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
  }
}
