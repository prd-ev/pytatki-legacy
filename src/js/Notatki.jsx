import React from "react";
import AddNote from "./AddNote.jsx";
import AddFolder from "./AddFolder.jsx";
import EditMode from "./EditMode.jsx";
import UsergroupList from "./UsergroupList.jsx";
import config from "../../config.json";
import style from "../scss/Notatki.scss";
import ConfirmDelete from "./ConfirmDelete.jsx";
import InfoNote from "./InfoNote.jsx";
import { ContextMenuTrigger } from "react-contextmenu";
import { ConnectedMenu, ConnectedGroupMenu } from "./ContextMenu.jsx";


const MENU_TYPE = "DYNAMIC";
function collect(props) {
  return props;
}

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      siteUrl: `http://${config.DEFAULT.HOST}:${config.DEFAULT.PORT}`,
      currentDepth: 0,
      data: [],
      currentPath: [],
      currentDirId: [],
      editModeOn: false,
      currentUsergroupName: "",
      is_note: null,
      note: null,
      infoVisible: false,
    };
    //Download root folders and set state of data[0] to array of folder objects
  }

  handleClick = (e, data, target) => {
    if (data.action === "Open") {
      this.openNote(data.name.slice(4));
    }
    if (data.action === "Properties") {
      this.infoNote(data.is_note, data.name.slice(4));
    }
    if (data.action === "Delete") {
      this.deleteNote_ContextMenu(data.name.slice(4));
    }
  };

  handleClickGroup = (e, data, target) => {
    if (data.action === "Properties") {
      this.infoNote(data.is_note, data.name);
    }
    if (data.action === "Delete") {
      this.deleteFolder_ContextMenu(data.name);
    }
  };

  deleteFolder_ContextMenu = id => {
    fetch(siteUrl + "/notegroup/" + id + "/delete/", {})
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  deleteNote_ContextMenu = id => {
    fetch(siteUrl + "/admin/delete/note/" + id, {})
      .then(response => response.text()) // if the response is a JSON object
      .then(success => console.log(success)) // Handle the success response object
      .catch(error => console.log(error)); // Handle the error response object
    this.updateContent();
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

  getUsergroupRoot = usergroupId => {
    const that = this;
    fetch(this.state.siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          this.state.siteUrl +
          "/api?query={getRootId(id_usergroup:" +
          usergroupId +
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
    return fetch(this.state.siteUrl + "/api?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          this.state.siteUrl +
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
  };

  openNote = e => {
    window.open(siteUrl + `/download/${e}`);
  };

  openNote = e => {
    let id = e.target.id.slice(4);
    window.open(this.state.siteUrl + `/download/${id}`);
  };

  openNoteClick = e => () => {
    window.open(siteUrl + `/download/${e}`);
  };

  infoNote = (is_note, id) => {
    this.setState({
      is_note: is_note,
      note: id,
      infoVisible: true
    });
  };

  closeInfo = () => {
    this.setState({
      is_note: null,
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
    let path = " ";
    for (const folder of this.state.currentPath) {
      path = path + "/" + folder;
    }
    return <span>{path}</span>;
  };

  packContent = () => {
    //Show content of current depth form state (this.state.data)
    if (this.state.currentUsergroupName) {
      if (this.state.data[this.state.currentDepth]) {
        var content = [];
        for (const value of this.state.data[this.state.currentDepth]) {
          if (value.is_note) {
            content.push(
              <div className={style.noteWrapper} key={value.key}>
                <div
                  className={style.note}
                  onClick={this.openNote}
                  id={value.key}
                >
                  <p>{value.title}</p>
                </div>
                <div className={style.delete}>
                  {this.state.editModeOn ? (
                    <i onClick={this.preDeleteNote} className="fas fa-times" />
                  ) : null}
                </div>
                <ContextMenuTrigger
                  id={MENU_TYPE}
                  holdToDisplay={1000}
                  name={value.key}
                  is_note={value.is_note}
                  onItemClick={this.handleClick}
                  collect={collect}
                  key={value.key}
                >
                  <div
                    id={value.key}
                    className={ComponentStyle.note}
                    onDoubleClick={this.openNoteClick(value.key.slice(4))}
                  >
                    <p>{value.title}</p>
                  </div>
                  <div
                    className={ComponentStyle.delete}
                    onClick={this.deleteNote}
                  >
                    {this.state.editModeOn ? (
                      <i className="fas fa-times" />
                    ) : null}
                  </div>
                </ContextMenuTrigger>
              </div>
            );
          } else {
            content.push(
              <div className={style.folderWrapper} key={value.key}>
                <div
                  className={style.folder}
                  onClick={this.changeCurrentDirectory}
                  id={value.key}
                >
                  <p>{value.title}</p>
                </div>
                <div className={style.delete}>
                  {this.state.editModeOn ? (
                    <i
                      onClick={this.preDeleteFolder}
                      className="fas fa-times"
                    />
                  ) : null}
                </div>
                <ContextMenuTrigger
                  id="NOTEGROUP"
                  holdToDisplay={1000}
                  name={value.key}
                  is_note={value.is_note}
                  onItemClick={this.handleClickGroup}
                  collect={collect}
                  key={value.key}
                >
                  <div
                    key={value.key}
                    className={ComponentStyle.folder}
                    onClick={this.changeCurrentDirectory}
                    id={value.key}
                  >
                    <p onClick={this.changeCurrentDirectory} id={value.key}>
                      {value.title}
                    </p>
                  </div>
                  <div
                    className={ComponentStyle.delete}
                    onClick={this.deleteFolder}
                  >
                    {this.state.editModeOn ? (
                      <i className="fas fa-times" />
                    ) : null}
                  </div>
                </ContextMenuTrigger>
              </div>
            );
          }
        }
        return content;
      } else {
        return (
          <p className={ComponentStyle.no_group_chosen}>
            Wybierz grupę aby kontynuować
          </p>
        );
      }
    }
  }

  changeMode = e => {
    e.preventDefault();
    this.setState(prevState => ({
      editModeOn: !prevState.editModeOn
    }));
  };

  preDeleteNote = e => {
    let note = e.target.parentElement.previousSibling.id.slice(4);
    this.setState({
      noteToDelete: note
    });
  };

  preDeleteFolder = e => {
    let folder = e.target.parentElement.previousSibling.id;
    this.setState({
      folderToDelete: folder
    });
  }

  deleteNote = e => {
    let noteId = e.target.previousSibling.id.slice(4);
    fetch(siteUrl + "/admin/delete/note/" + noteId, {})
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
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
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    this.updateContent();
  };

  updateContent = () => {
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
    let usergroupName = e.target.innerText;
    this.setState({
      currentDepth: 0,
      currentDirId: [],
      currentPath: [],
      currentUsergroupName: usergroupName
    });
  };

  render() {
    return (
      <React.Fragment>
        <UsergroupList
          updateUsergroup={this.updateCurrentUsergroup}
          siteUrl={this.state.siteUrl}
        />
        <div className={style.mainContent}>
          <p className={style.usergroupName}>
            {this.state.currentUsergroupName}
          </p>
          <div className={style.actionBar} key="actionBar">
            {this.state.currentUsergroupName ? <AddNote that={this} /> : ""}
            {this.state.currentUsergroupName ? <AddFolder that={this} /> : ""}
            {this.state.currentUsergroupName ? (
              <EditMode
                changeMode={this.changeMode}
                isOn={this.state.editModeOn}
              />
            ) : (
                ""
              )}
          </div>
          <ConfirmDelete
            //TODO:
            folderToDelete={this.state.folderToDelete}
            noteToDelete={this.state.noteToDelete}
            updateContent={this.updateContent}
            siteUrl={this.state.siteUrl}
            that={this}
          />
          {this.state.currentUsergroupName && this.state.currentDepth ? (
            <div className={style.back}>
              <i onClick={this.prevFolder} className="fas fa-arrow-left" />
              {this.showCurrentPath()}
            </div>
          ) : (
              ""
            )}
          <div className={style.fetchedData} key="fetchedData">
            {this.packContent()}
          </div>
          <InfoNote
            note={this.state.note}
            is_note={this.state.is_note}
            visible={this.state.infoVisible}
            closeInfoNotatki={this.closeInfo}
          />
          <ConnectedMenu />
          <ConnectedGroupMenu />
        </div>
      </React.Fragment>
    );
  }
}

export default Notatki;
