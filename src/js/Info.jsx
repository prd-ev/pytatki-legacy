import React from "react";

const siteUrl = "http://127.0.0.1:5000";

class Info extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      noteInfo: {}
    }
  }

  getNote(id){
    fetch(siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            "/api?query={getNoteById(id_note:" +
            id +
            ',access_token:"' +
            token +
            '")}'
        )
          .then(response => {
            return response.json();
          })
          //.then(response => response.data.json())
          .then(response => {
            return JSON.parse(response.data.getNoteById)
          })
          .then(noteId => {
            console.log(noteId);
            this.setState({
              noteInfo: noteId
            });
            console.log("setstate")
          })
      );
  }

  shouldComponentUpdate(nextProps, nextState){
    if (this.props.note !== nextProps.note) {
      return true
    }
    else
    {
      if (this.state.noteInfo !== {}) {
        if (this.state.noteInfo.idnote !== nextState.noteInfo.idnote)
          return true;
      }
    }
    return false
  }

  componentDidUpdate(){
    this.getNote(this.props.note)
  }

  packNote = () => {
    return <div>{ JSON.stringify(this.state.noteInfo) }</div >
  }

  render(){
    return (
      <div id="info">
      <div>oh {String(this.props.note)}</div>
      {this.packNote()}
      </div>
    )
  }
}

export default Info;