import React from "react";
import config from "../../config.json";
import ComponentStyle from "../scss/Info.scss";

const siteUrl = "http://" + config.DEFAULT.HOST + ":" + config.DEFAULT.PORT;

class InfoNote extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      noteInfo: null,
      noteActions: null,
      groupInfo: null,
      groupContent: null
    };
  }

  closeInfo = () => {
    //Remove data from states
    this.setState({
      noteInfo: null,
      noteActions: null,
      groupInfo: null,
      groupContent: null
    });
    //Run function to remove states of parent
    this.props.closeInfoNotatki();
  };

  //Fetch from /api/?query={getNoteById} of note id in props an token passed as argument
  getNote = token => {
    if (this.props.note != null)
      return fetch(
        siteUrl +
          "/api/?query={getNoteById(id_note:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          //Convert response to json
          return response.json();
        })
        .then(response => {
          //Filter data
          return JSON.parse(response.data.getNoteById);
        });
  };

  //Fetch from /api/?query={getNoteLastActions} of note id in props and token passed as argument
  getNoteLastActions = token => {
    if (this.props.note != null)
      return fetch(
        siteUrl +
          "/api/?query={getNoteLastActions(id_note:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          //Convert data to json
          return response.json();
        })
        .then(response => {
          //Filter data
          return JSON.parse(response.data.getNoteLastActions);
        });
  };

  //Fetch from /api/?query={getNotegroupById} of note id in props an token passed as argument
  getNotegroup = token => {
    if (this.props.note != null)
      return fetch(
        siteUrl +
          "/api/?query={getNotegroupById(notegroup_id:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          //Convert response to json
          return response.json();
        })
        .then(response => {
          //Filter data
          return JSON.parse(response.data.getNotegroupById);
        });
  };

  //Fetch from /api/?query={getContent} of note id in props an token passed as argument
  getContent = token => {
    if (this.props.note != null)
      return fetch(
        siteUrl +
          "/api/?query={getContent(id_notegroup:" +
          this.props.note +
          ',access_token:"' +
          token +
          '")}'
      )
        .then(response => {
          //Convert response to json
          return response.json();
        })
        .then(response => {
          //Filter data
          return JSON.parse(response.data.getContent);
        });
  };

  //Fetch data of note from api and set to state
  fetchData = () => {
    if (this.props.is_note) {
      if (
        this.state.noteInfo == null &&
        this.state.noteActions == null &&
        this.props.note != null
      ) {
        fetch(siteUrl + "/api/?query={getToken}")
          .then(response => response.json())
          .then(res => res.data.getToken)
          .then(token => {
            this.getNote(token).then(info => {
              if (info)
                this.getNoteLastActions(token).then(actions => {
                  if (actions)
                    this.setState({
                      noteInfo: info,
                      noteActions: actions
                    });
                });
            });
          });
      }
    } else {
      if (
        this.state.groupInfo == null &&
        this.state.groupContent == null &&
        this.props.note != null
      ) {
        fetch(siteUrl + "/api/?query={getToken}")
          .then(response => response.json())
          .then(res => res.data.getToken)
          .then(token => {
            this.getContent(token).then(content => {
              if (content)
                this.getNotegroup(token).then(info => {
                  if (info)
                    this.setState({
                      groupInfo: info,
                      groupContent: content
                    });
                });
            });
          });
      }
    }
  };

  //Check if component should update: if visible changes or if noteInfo changes
  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.visible !== nextProps.visible) {
      return true;
    }
    if (this.state.noteInfo !== nextState.noteInfo) {
      return true;
    }
    if (this.state.groupInfo !== nextState.groupInfo) {
      return true;
    }
    return false;
  }

  //If component updated fetch new data
  componentDidUpdate() {
    this.fetchData();
  }

  //Opens note in new window
  openNote = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  //Renders info about notegroup
  renderGroupHeader = () => {
    if (this.state.groupInfo != null) {
      return (
        <React.Fragment>
          <h2>{this.state.groupInfo.name}</h2>
        </React.Fragment>
      );
    }
    return (
      <div>
        <br />
        <i className="ld ld-ring ld-cycle" />
      </div>
    );
  };

  //Renders numbers of notes in notegroup
  renderGroupElements = () => {
    if (this.state.groupContent != null) {
      return (
        <React.Fragment>
          <h2>{this.state.groupContent.length} notes</h2>
        </React.Fragment>
      );
    }
    return (
      <div>
        <br />
        <i className="ld ld-ring ld-cycle" />
      </div>
    );
  };

  //Renders header of info component
  renderNoteHeader = () => {
    if (this.state.noteInfo != null) {
      return (
        <React.Fragment>
          <h2>
            <b>{this.state.noteInfo.title}</b> by{" "}
            {this.state.noteInfo.creator_login}
          </h2>
          <p onClick={this.openNote(this.state.noteInfo.idnote)}>
            EDIT <i className="fas fa-edit" />
          </p>
        </React.Fragment>
      );
    }
    return (
      <div>
        <br />
        <i className="ld ld-ring ld-cycle" />
      </div>
    );
  };

  //Render actions
  renderNoteActions = () => {
    if (this.state.noteActions != null) {
      return this.state.noteActions.map(action => (
        <div key={action.idaction}>
          {action.content} {action.date}
        </div>
      ));
    }
    return (
      <div>
        <br />
        <i className="ld ld-ring ld-cycle" />
      </div>
    );
  };

  render() {
    if (this.props.visible) {
      if (this.props.is_note) {
        return (
          <React.Fragment>
            <div className={ComponentStyle.info}>
              <i onClick={() => this.closeInfo()} className="fas fa-times" />
              {this.renderNoteHeader()}
              <h3>Latest actions</h3>
              {this.renderNoteActions()}
            </div>
          </React.Fragment>
        );
      } else {
        return (
          <React.Fragment>
            <div className={ComponentStyle.info}>
              <i onClick={() => this.closeInfo()} className="fas fa-times" />
              {this.renderGroupHeader()}
              {this.renderGroupElements()}
            </div>
          </React.Fragment>
        );
      }
    } else {
      return <React.Fragment />;
    }
  }
}

export default InfoNote;
