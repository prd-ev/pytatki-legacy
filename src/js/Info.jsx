import React from "react";
import ComponentStyle from "../scss/Info.scss";

const siteUrl = "http://127.0.0.1:5000";

class Info extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      noteInfo: null,
      noteActions: null
    };
  }

  closeInfo() {
    this.props.closeInfo();
    this.setState({
      noteInfo: null,
      noteActions: null
    });
  }

  getNote(token) {
    if (this.state.noteInfo == null && this.props.note != null) {
      return fetch(
        siteUrl +
          "/api/?query={getNoteById(id_note:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          return response.json();
        })
        .then(response => {
          return JSON.parse(response.data.getNoteById);
        });
    }
  }

  getNoteLastActions(token) {
    if (this.state.noteActions == null && this.props.note != null) {
      return fetch(
        siteUrl +
          "/api/?query={getNoteLastActions(id_note:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          return response.json();
        })
        .then(response => {
          return JSON.parse(response.data.getNoteLastActions);
        });
    }
  }

  fetchData() {
    fetch(siteUrl + "/api/?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => {
        this.getNote(token).then(info => {
          this.getNoteLastActions(token).then(actions => {
            this.setState({
              noteInfo: info,
              noteActions: actions
            });
          });
        });
      });
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.visible !== nextProps.visible) {
      return true;
    }
    if (this.state.noteInfo !== nextState.noteInfo) {
      return true;
    }
    return false;
  }

  componentDidUpdate() {
    this.fetchData();
  }

  openNote = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  packNote = () => {
    if (this.state.noteInfo !== null) {
      if (this.state.noteInfo.idnote != null && this.props.visible) {
        return (
          <div className={ComponentStyle.info}>
            <i onClick={() => this.closeInfo()} className="fas fa-times" />
            <h2>
              <b>{this.state.noteInfo.title}</b> by{" "}
              {this.state.noteInfo.creator_login}
            </h2>
            <p onClick={this.openNote(this.state.noteInfo.idnote)}>
              EDIT <i className="fas fa-edit" />
            </p>
            <h3>Latest actions</h3>
            {this.state.noteActions.map(action => (
              <div key={action.idaction}>
                {action.content} {action.date}
              </div>
            ))}
          </div>
        );
      }
    }
    return <div />;
  };

  render() {
    return <div id="info">{this.packNote()}</div>;
  }
}

export default Info;
