import React from "react";

const siteUrl = "http://127.0.0.1:5000";

class Info extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      noteInfo: {},
      noteActions: [],
      visible: this.props.visible
    };
    this.hideInfo = this.hideInfo.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    // You don't have to do this check first, but it can help prevent an unneeded render
    if (nextProps.visible !== this.state.visible) {
      this.setState({ visible: nextProps.visible });
    }
  }

  hideInfo() {
    this.setState({ visible: false, noteInfo: {}, noteActions: [] });
  }

  getNote(id) {
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
            return JSON.parse(response.data.getNoteById);
          })
          .then(noteId => {
            this.setState({
              noteInfo: noteId
            });
          })
      );
  }

  getNoteLastActions(id) {
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
            console.log(response);
            return response.json();
          })
          //.then(response => response.data.json())
          .then(response => {
            console.log(response);
            return response.data.getNoteLastActions;
          })
          .then(noteActions => {
            console.log(noteActions);
            this.setState({
              noteActions: noteActions
            });
          })
      );
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.note !== nextProps.note) {
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
        if (this.state.visible != nextState.visible) {
          return true;
        }
      }
    }
    return false;
  }

  componentDidUpdate() {
    this.getNote(this.props.note);
    this.getNoteLastActions(this.props.note);
  }

  openNote = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  packNote = () => {
    if (this.state.noteInfo.idnote != null && this.state.visible) {
      return (
        <div /*style="border-style: dashed"*/>
          <button onClick={this.hideInfo}>X</button>
          <h2>
            <b>{this.state.noteInfo.title}</b> by{" "}
            {this.state.noteInfo.creator_login}
          </h2>
          <button onClick={this.openNote(this.state.noteInfo.idnote)}>
            OPEN
          </button>
          <br />
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
