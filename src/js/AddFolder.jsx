import React, { Component } from 'react'
import ComponentStyle from '../scss/AddContent.scss'

export default class AddFolder extends Component {
    constructor(props) {
      super(props)
    }
    
  render() {
    return (
      <form id="addFolderForm" className={ComponentStyle.form} onSubmit={this.props.addFolder}>
          <label> Dodaj folder w aktualnej lokalizacji </label>
          <input required name="title" type="text"/>
          <input type="submit" value="Dodaj"/>
      </form>
    )
  }
}
