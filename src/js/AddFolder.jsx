import React, { Component } from 'react'

export default class AddFolder extends Component {
    constructor(props) {
      super(props)
    
      this.state = {
      }
    }
    
  render() {
    return (
      <form id="addFolderForm" onSubmit={this.props.addFolder}>
          <input required name="title" type="text"/>
          <input type="submit" value="Dodaj folder w aktualnej lokalizacji"/>
      </form>
    )
  }
}
