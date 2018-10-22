import React from "react";
import ComponentStyle from "../scss/Info.scss";

const siteUrl = "http://127.0.0.1:5000";

class Info extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      noteInfo: {},
      noteActions: []
    };
  }

  getNote(id) {
    let note = null;
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
          .then(response => {
            return JSON.parse(response.data.getNoteById);
          })
          .then(noteId => {
            this.setState({
              noteInfo: noteId
            });
            note = noteId
          })
      );
  return note
  }

  getNoteLastActions(id) {
    let actions = null
    fetch(siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            "/api?query={getNoteLastActions(id_note:" +
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
            return response.data.getNoteLastActions;
          })
          .then(noteActions => {
            this.setState({
              noteActions: noteActions
            });
          })
      );
  return actions
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.visible !== nextProps.visible) {
      return true;
    } else {
      if (nextState.noteActions == {} && nextState.noteInfo == {}) {
        return false;
      } else {
        if (this.state.noteInfo !== {}) {
          if (
            this.state.noteInfo.idnote !== nextState.noteInfo.idnote ||
            this.state.noteActions != nextState.noteActions
          )
            return true;
        }
    if (this.props.note !== nextProps.note) {
          return true;
        }
      }
    }
    return false;
  }

  componentDidUpdate() {
    let note = this.getNote(this.props.note);
    console.log(note);
    let actions = this.getNoteLastActions(this.props.note);
    console.log(actions)
  }

  openNote = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  packNote = () => {
    if (this.state.noteInfo.idnote != null && this.props.visible) {
      return (
        <div className={ComponentStyle.info}>
          <i onClick={() => this.props.closeInfo()} class="fas fa-times">X</i>
          <h2>
            <b>{this.state.noteInfo.title}</b> by{" "}
            {this.state.noteInfo.creator_login}
          </h2>
          <p onClick={this.openNote(this.state.noteInfo.idnote)}>
            EDIT <i class="fas fa-edit" />
          </p>
          <h3>Latest actions</h3>
          {this.state.noteActions}
        </div>
      );
    }
    return <div />;
  };

  render() {
    return <div id="info">{this.packNote()}</div>;
  }
}

export default Info;
