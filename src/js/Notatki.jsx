import React from "react";
import AddNote from "./AddNote.jsx";
import AddFolder from "./AddFolder.jsx";
import EditMode from "./EditMode.jsx";
import NotegroupList from "./UsergroupList.jsx";
import Info from "./Info.jsx";
import {
  ContextMenuTrigger,
  ContextMenu,
  MenuItem,
  connectMenu
} from "react-contextmenu";

const siteUrl = "http://127.0.0.1:5000";
const MENU_TYPE = "DYNAMIC";
function collect(props) {
  return props;
}

const DynamicMenu = props => {
  const { id, trigger } = props;
  const handleItemClick = trigger ? trigger.onItemClick : null;

  return (
    <ContextMenu id={id}>
      {trigger && (
        <MenuItem onClick={handleItemClick} data={{ action: "Open" }}>
          Otwórz
        </MenuItem>
      )}
      {trigger && (
        <MenuItem onClick={handleItemClick} data={{ action: "Properties" }}>
          Właściwości
        </MenuItem>
      )}
    </ContextMenu>
  );
};

const ConnectedMenu = connectMenu(MENU_TYPE)(DynamicMenu);

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentDepth: 0,
      data: [],
      currentPath: [],
      currentDirId: [],
      editModeOn: false,
      note: null,
      infoVisible: false
    };
    //Download root folders and set state of data[0] to array of folder objects
  }

  handleClick = (e, data, target) => {
    if (data.action === "Open") {
      this.openNote(data.name.slice(4));
    }
    if (data.action === "Properties") {
      this.infoNote(data.name.slice(4));
    }
  };

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
        } else {
          object["title"] = notegroup.folder_name;
          object["key"] = notegroup.idnotegroup;
          object["is_note"] = false;
          folderContent.push(object);
        }
      }
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
    });
  };

  getUsergroupRoot(usergroup) {
    const that = this;
    fetch(siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            "/api?query={getRootId(id_usergroup:" +
            usergroup +
            ',access_token:"' +
            token +
            '")}'
        )
          .then(response => response.json())
          .then(myJson => Number(myJson.data.getRootId))
          .then(rootId => {
            that.setState({
              currentDirId: [rootId]
            });
            that.updateContent(rootId);
          })
      );
  }

  getContent(dir_id) {
    return fetch(siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            "/api?query={getContent(id_notegroup:" +
            dir_id +
            ',access_token:"' +
            token +
            '")}'
        )
      )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))

      .catch(error => console.log(error));
  }

  openNote(e) {
    window.open(siteUrl + `/download/${e}`);
  }

  openNoteClick = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  infoNote(id) {
    this.setState({ note: id, infoVisible: true });
  }

  closeInfo() {
    this.setState({
      note: null,
      infoVisible: false
    });
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
  };

  showCurrentPath = () => {
    //Show current path from state
    let path = "";
    for (const folder of this.state.currentPath) {
      path = path + " / " + folder;
    }
    return <h5>{path}</h5>;
  };

  packContent = () => {
    //Show content of current depth form state (this.state.data)
    if (this.state.data[this.state.currentDepth]) {
      var content = [];
      for (const value of this.state.data[this.state.currentDepth]) {
        if (value.is_note) {
          content.push(
            <ContextMenuTrigger
              id={MENU_TYPE}
              holdToDisplay={1000}
              name={value.key}
              onItemClick={this.handleClick}
              collect={collect}
              key={value.key}
            >
              <h1
                id={value.key}
                onDoubleClick={this.openNoteClick(value.key.slice(4))}
              >
                {"Notatka " + value.title}
              </h1>
              <span onClick={this.deleteNote}>
                {this.state.editModeOn ? " x" : null}
              </span>
            </ContextMenuTrigger>
          );
        } else {
          content.push(
            <div key={value.key}>
              <h1 onClick={this.changeCurrentDirectory} id={value.key}>
                {value.title}
              </h1>
              <span onClick={this.deleteFolder}>
                {this.state.editModeOn ? " x " : null}
              </span>
            </div>
          );
        }
      }
      return content;
    }
    return null;
  };

  uploadNote = e => {
    e.preventDefault();
    const form = document.getElementById("form");
    const file = form[1].files[0];
    const title = form[0].value;
    var formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);
    formData.append(
      "notegroup_id",
      this.state.currentDirId[this.state.currentDepth]
    );
    fetch(siteUrl + "/add/", {
      method: "POST",
      body: formData
    })
      .then(
        response => response.text() // if the response is a JSON object
      )
      .then(
        success => console.log(success) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  addFolder = e => {
    e.preventDefault();
    var formData = new FormData();
    formData.append("title", document.getElementById("addFolderForm")[0].value);
    formData.append(
      "parent_id",
      this.state.currentDirId[this.state.currentDirId.length - 1]
    );
    formData.append("class", "1"); //dodać dynamicznie
    fetch(siteUrl + "/admin/add/", {
      method: "POST",
      body: formData
    })
      .then(
        response => response.text() // if the response is a JSON object
      )
      .then(
        success => console.log(success) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  changeMode = e => {
    e.preventDefault();
    this.setState(prevState => ({
      editModeOn: !prevState.editModeOn
    }));
  };

  deleteNote = e => {
    let noteId = e.target.previousSibling.id.slice(4);
    fetch(siteUrl + "/admin/delete/note/" + noteId, {})
      .then(
        response => response.text() // if the response is a JSON object
      )
      .then(
        success => console.log(success) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  deleteFolder = e => {
    let folderId = e.target.previousSibling.id;
    fetch(siteUrl + "/notegroup/" + folderId + "/delete/", {})
      .then(
        response => response.text() // if the response is a JSON object
      )
      .then(
        success => console.log(success) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  updateContent() {
    const that = this;
    this.getContent(
      this.state.currentDirId[this.state.currentDirId.length - 1]
    ).then(innerJson => {
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
        } else {
          object["title"] = notegroup.folder_name;
          object["key"] = notegroup.idnotegroup;
          object["is_note"] = false;
          folderContent.push(object);
        }
      }
      let updated_data = that.state.data;
      updated_data[that.state.currentDepth] = folderContent;
      that.setState({
        data: updated_data
      });
    });
  }

  updateCurrentUsergroup = e => {
    this.getUsergroupRoot(e.target.id);
    this.setState({
      currentDepth: 0,
      currentDirId: [],
      currentPath: []
    });
  };

  render() {
    return (
      <div>
        <NotegroupList updateUsergroup={this.updateCurrentUsergroup} />
        <AddNote uploadNote={this.uploadNote} />
        <AddFolder addFolder={this.addFolder} />
        <EditMode changeMode={this.changeMode} isOn={this.state.editModeOn} />
        <Info
          note={this.state.note}
          visible={this.state.infoVisible}
          closeInfo={this.closeInfo.bind(this)}
        />
        <h1 onClick={this.prevFolder}>Cofnij</h1>
        {this.showCurrentPath()}
        {this.packContent()}
        <ConnectedMenu />
      </div>
    );
  }
}

export default Notatki;
