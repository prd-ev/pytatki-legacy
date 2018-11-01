import React from "react";
import config from "../../config.json";
import ComponentStyle from "../scss/Info.scss";

const siteUrl = "http://" + config.default.host + ":" + config.default.port;

class InfoNoteGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      groupInfo: null,
      groupContent: null
    };
  }

  closeInfo = () => {
    //Remove data from states
    this.setState({
      groupInfo: null,
      groupContent: null
    });
    //Run function to remove states of parent
    this.props.closeInfoGroupNotatki();
  };

  //Fetch from /api/?query={getNotegroupById} of note id in props an token passed as argument
  getNotegroup = token => {
    if (this.props.notegroup != null)
      return fetch(
        siteUrl +
          "/api/?query={getNotegroupById(id_notegroup:" +
          this.props.notegroup +
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

  //Fetch from /api/?query={getContent} of note id in props an token passed as argument
  getContent = token => {
    if (this.props.notegroup != null)
      return fetch(
        siteUrl +
          "/api/?query={getContent(id_notegroup:" +
          this.props.notegroup +
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

  fetchData = () => {
    if (this.state.groupInfo == null && this.props.notegroup != null) {
      fetch(siteUrl + "/api/?query={getToken}")
        .then(response => response.json())
        .then(res => res.data.getToken)
        .then(token => {
          if (this.getContent(token))
            this.getContent(token).then(content => {
              this.getNotegroup(token).then(info => {
                this.setState({ groupInfo: info, groupContent: content });
              });
            });
        });
    }
  };

  //Check if component should update: if visible changes or if noteInfo changes
  shouldComponentUpdate(nextProps, nextState) {
    if (this.props.visible !== nextProps.visible) {
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

  //Renders header of info component
  renderHeader = () => {
    if (this.state.noteInfo != null) {
      return (
        <React.Fragment>
          <h2>
            <b>{this.state.groupInfo.name}</b>
            <br />
            {this.state.groupContent.length} {"elements"}
          </h2>
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

  render() {
    if (this.props.visible) {
      return (
        <React.Fragment>
          <div className={ComponentStyle.info}>
            <i onClick={() => this.closeInfo()} className="fas fa-times" />
            {this.renderHeader()}
          </div>
        </React.Fragment>
      );
    } else {
      return <React.Fragment />;
    }
  }
}

export default InfoNoteGroup;
