import React from "react";
//import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentDepth: 0,
      data: [],
    };
  }

  componentWillMount() {
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getRootId(id_usergroup:3,access_token:"' + token + '")}')
        .then(response => response.json())
        .then(myJson => myJson.data.getRootId)
        .then(myJson => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + Number(myJson) + ',access_token:"' + token + '")}'))
        .then(response => response.json())
        .then(myJson => JSON.parse(myJson.data.getContent))
      )
      .then(function (innerJson) {
        let rootFolders = [];
        for (let notegroup of innerJson) {
          let object = {};
          object["title"] = notegroup.folder_name;
          if (notegroup.idnote) {
            object["key"] = "note" + notegroup.idnote;
          } else {
            object["key"] = notegroup.idnotegroup;
          }
          rootFolders.push(object);
        };
        let updated_data = that.state.data;
        updated_data[0] = rootFolders;
        that.setState({ data: updated_data });
      })
      .catch(error => console.log(error));
  }


  changeCurrentDirectory = e => {
    let selected_subject = e.target.id;
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + selected_subject + ',access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .then(function (innerJson) {
        let content = [];
        for (let notegroup of innerJson) {
          let object = {};
          object["title"] = notegroup.folder_name;
          if (notegroup.idnote) {
            object["key"] = "note" + notegroup.idnote;
          } else {
            object["key"] = notegroup.idnotegroup;
          }
          content.push(object);
        };
        let updated_data = that.state.data;
        updated_data[that.state.currentDepth + 1] = content;
        that.setState({ data: updated_data, currentDepth: that.state.currentDepth + 1 });
      })
      .catch(error => console.log(error));
  };

  packContent = () => {
    if (this.state.data[this.state.currentDepth]) {
      var content = [];
      for (let value of this.state.data[this.state.currentDepth]) {
        content.push(<h1 onClick={this.changeCurrentDirectory} id={value.key} key={value.key}>
          {value.title}
        </h1>);
      }
      return content;
    }
    return null;
  };

  // That was first in render
  //<AddNote rootFolders={this.state.rootFolders} update={this.updateNotes} />
  render() {
    return (<div>
      {this.packContent()}
    </div>);
  };
}

export default Notatki;
