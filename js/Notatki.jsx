import React from "react";
import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentDepth: 0,
      data: [],
      currentPath: [],
      currentDirId: "2"//mock
    };
  }

  componentWillMount() {
    //Download root folders and set state of data[0] to array of folder objects
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
        for (const notegroup of innerJson) {
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
    //Increase depth, set state of data[depth] to downloaded array of folder/note object
    let selected_dir_id = e.target.id;
    let selected_dir_name = e.target.innerText;
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + selected_dir_id + ',access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .then(function (innerJson) {
        let folderContent = [];
        for (const notegroup of innerJson) {
          let object = {};
          if (notegroup.idnote) {
            object["title"] = notegroup.name;
            object["key"] = "note" + notegroup.idnote;
            object["is_note"] = true;
          } else {
            object["title"] = notegroup.folder_name;
            object["key"] = notegroup.idnotegroup;
            object["is_note"] = false;
          }
          folderContent.push(object);
        };
        let updated_data = that.state.data;
        updated_data[that.state.currentDepth + 1] = folderContent;
        let updated_path = that.state.currentPath;
        updated_path[that.state.currentDepth] = selected_dir_name;
        that.setState({ data: updated_data, currentDepth: that.state.currentDepth + 1, currentPath: updated_path, currentDirId: selected_dir_id });
      })
      .catch(error => console.log(error));
  };

  openNote = (e) => {
    console.log("Jak wyświetlić notatkę?");
    
    let id = e.target.id.slice(4);
    window.open(`http://127.0.0.1:5000/download/${id}`);
  }

  prevFolder = () => {
    //Update current path and decrease depth (if 1 or higher)
    let path = this.state.currentPath;
    let depth = this.state.currentDepth;
    path.pop();
    if (!this.state.currentDepth < 1) {
      depth -= 1;
    }
    this.setState({
      currentDepth: depth,
      currentPath: path
    });
  }

  showCurrentPath = () => {
    //Show current path from state
    let path = "";
    for (const folder of this.state.currentPath) {
      path = path + " / " + folder;
    }
    return <h5>{path}</h5>
  }

  packContent = () => {
    //Show content of current depth form state (this.state.data)
    if (this.state.data[this.state.currentDepth]) {
      var content = [];
      for (const value of this.state.data[this.state.currentDepth]) {
        if (value.is_note) {
          content.push(<h1 onClick={this.openNote} id={value.key} key={value.key}>
            {"Notatka " + value.title}
          </h1>);
        } else {
          content.push(<h1 onClick={this.changeCurrentDirectory} id={value.key} key={value.key}>
            {value.title}
          </h1>);
        }
      }
      return content;
    }
    return null;
  };

  uploadNote = (e) => {
    e.preventDefault();
    const form = document.getElementById('form');
    const file = form[1].files[0];
    const title = form[0].value;
    var formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    formData.append('notegroup_id', this.state.currentDirId);
    fetch('http://127.0.0.1:5000/add/', {
      method: 'POST',
      body: formData
    }).then(
      response => response.text() // if the response is a JSON object
    ).then(
      success => console.log(success) // Handle the success response object
    ).catch(
      error => console.log(error) // Handle the error response object
    );
  }

  render() {
    return (
      <div>
        <AddNote uploadNote={this.uploadNote}></AddNote>
        <h1 onClick={this.prevFolder}>Cofnij</h1>
        {this.showCurrentPath()}
        {this.packContent()}
      </div>
    );
  };
}

export default Notatki;
