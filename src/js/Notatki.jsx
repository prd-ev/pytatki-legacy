import React from "react";
import AddNote from "./AddNote.jsx";
import AddFolder from './AddFolder.jsx';
import EditMode from './EditMode.jsx';
import NotegroupList from './UsergroupList.jsx';
import config from '../../config.json';
import ComponentStyle from '../scss/Notatki.scss';
import ConfirmDelete from './ConfirmDelete.jsx';

const siteUrl = "http://" + config.default.host + ":" + config.default.port;

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentDepth: 0,
      data: [],
      currentPath: [],
      currentDirId: [],
      editModeOn: false,
      currentUsergroupName: "",
    };
    //Download root folders and set state of data[0] to array of folder objects
  }

  changeCurrentDirectory = e => {
    //Increase depth, set state of data[depth] to downloaded array of folder/note object
    let selected_dir_id = e.target.id;
    let selected_dir_name = e.target.innerText;
    const that = this;
    this.getContent(selected_dir_id).then(innerJson => {
      let folderContent = [];
      for (const notegroup of innerJson) {
        let object = {};
        if (notegroup.idnote) {
          if (notegroup.status_id != 2) {
            object["title"] = notegroup.name;
            object["key"] = "note" + notegroup.idnote;
            object["is_note"] = true;
            folderContent.push(object);
          }
        }
        else {
          object["title"] = notegroup.folder_name;
          object["key"] = notegroup.idnotegroup;
          object["is_note"] = false;
          folderContent.push(object);
        }
      }
      ;
      let updated_data = that.state.data;
      updated_data[that.state.currentDepth + 1] = folderContent;
      let updated_path = that.state.currentPath;
      updated_path[that.state.currentDepth] = selected_dir_name;
      let updated_dir_id = that.state.currentDirId;
      updated_dir_id[that.state.currentDepth + 1] = Number(selected_dir_id);
      that.setState(prevState => ({
        data: updated_data,
        currentDepth: prevState.currentDepth + 1,
        currentPath: updated_path,
        currentDirId: updated_dir_id
      }));
    }
    );
  };

  getUsergroupRoot(usergroupId) {
    const that = this;
    fetch(siteUrl + '/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch(siteUrl + '/api?query={getRootId(id_usergroup:' + usergroupId + ',access_token:"' + token + '")}')
        .then(response => response.json())
        .then(myJson => Number(myJson.data.getRootId))
        .then(rootId => {
          that.setState({
            currentDirId: [rootId]
          });
          that.updateContent(rootId);
        }));
  }

  getContent(dir_id) {
    return fetch(siteUrl + '/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch(siteUrl + '/api?query={getContent(id_notegroup:' + dir_id + ',access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))

      .catch(error => console.log(error));
  }


  openNote = (e) => {
    let id = e.target.id.slice(4);
    window.open(siteUrl + `/download/${id}`);
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
    let path = " ";
    for (const folder of this.state.currentPath) {
      path = path + "/" + folder;
    }
    return <span>{path}</span>
  }

  packContent = () => {
    //Show content of current depth form state (this.state.data)
    if (this.state.currentUsergroupName) {
      if (this.state.data[this.state.currentDepth]) {
        var content = [];
        for (const value of this.state.data[this.state.currentDepth]) {
          if (value.is_note) {
            content.push(<div className={ComponentStyle.noteWrapper} key={value.key}><div className={ComponentStyle.note} onClick={this.openNote} id={value.key}><p>
              {value.title}
            </p></div>
              <div className={ComponentStyle.delete} onClick={this.preDeleteNote}>
                {this.state.editModeOn ? <i className="fas fa-times"></i> : null}
              </div>
            </div>);
          } else {
            content.push(<div className={ComponentStyle.folderWrapper} key={value.key}><div className={ComponentStyle.folder} onClick={this.changeCurrentDirectory} id={value.key}><p>
              {value.title}
            </p></div>
              <div className={ComponentStyle.delete} onClick={this.preDeleteFolder}>
                {this.state.editModeOn ? <i className="fas fa-times"></i> : null}
              </div>
            </div>);
          }
        }
        return content;
      }
    } else {
      return <p className={ComponentStyle.no_group_chosen}>Wybierz grupę aby kontynuować</p>
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
    formData.append('notegroup_id', this.state.currentDirId[this.state.currentDepth]);
    fetch(siteUrl + '/add/', {
      method: 'POST',
      body: formData
    }).then(
      response => response.json() // if the response is a JSON object
    ).then(
      success => alert(success.data) // Handle the success response object
    ).catch(
      error => console.log(error) // Handle the error response object
    );
    this.updateContent();
    e.target.querySelector("input").value = null;
    e.target.querySelector("#file").value = null;
  }

  addFolder = (e) => {
    e.preventDefault();
    var formData = new FormData();
    formData.append('title', document.getElementById('addFolderForm')[0].value);
    formData.append('parent_id', this.state.currentDirId[this.state.currentDirId.length - 1]);
    formData.append('class', '1');//dodać dynamicznie 
    fetch(siteUrl + '/admin/add/', {
      method: 'POST',
      body: formData
    }).then(
      response => response.json() // if the response is a JSON object
    ).then(
      success => alert(success.data) // Handle the success response object
    ).catch(
      error => console.log(error) // Handle the error response object
    );
    this.updateContent();
    e.target.querySelector("input").value = null;
  }

  changeMode = (e) => {
    e.preventDefault();
    this.setState(prevState => ({
      editModeOn: !prevState.editModeOn
    }))
  }

  preDeleteNote = e => {
    let note = e.target.parentElement.previousSibling.id.slice(4);
    this.setState({
      noteToDelete: note
    })
  }

  preDeleteFolder = e => {
    let folder = e.target.parentElement.previousSibling.id;
    this.setState({
      folderToDelete: folder
    })
  }

  

  updateContent() {
    const that = this;
    this.getContent(this.state.currentDirId[this.state.currentDirId.length - 1])
      .then(innerJson => {
        let folderContent = [];
        for (const notegroup of innerJson) {
          let object = {};
          if (notegroup.idnote) {
            if (notegroup.status_id != 2) {
              object["title"] = notegroup.name;
              object["key"] = "note" + notegroup.idnote;
              object["is_note"] = true;
              folderContent.push(object);
            }
          }
          else {
            object["title"] = notegroup.folder_name;
            object["key"] = notegroup.idnotegroup;
            object["is_note"] = false;
            folderContent.push(object);
          }
        }
        let updated_data = that.state.data;
        updated_data[that.state.currentDepth] = folderContent;
        that.setState({
          data: updated_data,
        });
      });
  }

  updateCurrentUsergroup = e => {
    this.getUsergroupRoot(e.target.id);
    let usergroupName = e.target.innerText;
    this.setState({
      currentDepth: 0,
      currentDirId: [],
      currentPath: [],
      currentUsergroupName: usergroupName
    })
  }

  render() {
    return (
      <React.Fragment>
        <NotegroupList updateUsergroup={this.updateCurrentUsergroup} siteUrl={siteUrl}></NotegroupList>
        <div className={ComponentStyle.mainContent}>
          <p>{this.state.currentUsergroupName}</p>
          <div className={ComponentStyle.actionBar} key="actionBar">
            {this.state.currentUsergroupName ? (
              <AddNote uploadNote={this.uploadNote}></AddNote>
            ) : ("")}
            {this.state.currentUsergroupName ? (
              <AddFolder addFolder={this.addFolder}></AddFolder>
            ) : ("")}
            {this.state.currentUsergroupName ? (
              <EditMode changeMode={this.changeMode} isOn={this.state.editModeOn}></EditMode>
            ) : ("")}
          </div>
          <ConfirmDelete folderToDelete={this.state.folderToDelete} noteToDelete={this.state.noteToDelete} updateContent={this.updateContent} siteUrl={siteUrl} that={this} ></ConfirmDelete>
          {this.state.currentUsergroupName && this.state.currentDepth ? (
            <div className={ComponentStyle.back}>
              <i onClick={this.prevFolder} className="fas fa-arrow-left"></i>
              {this.showCurrentPath()}
            </div>
          ) : ("")}
          <div className={ComponentStyle.fetchedData} key="fetchedData">
            {this.packContent()}
          </div>
        </div>
      </React.Fragment>
    );
  };
}

export default Notatki;
