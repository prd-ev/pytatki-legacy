import React from "react";
import EditMode from "./EditMode.jsx";
import UsergroupList from "./UsergroupList.jsx";
import config from "../../config.json";
import style from "../scss/Notatki.scss";
import ConfirmDelete from "./ConfirmDelete.jsx";
import InfoNote from "./InfoNote.jsx";
import ListOfUsers from "./ListOfUsers.jsx";
import { ContextMenuTrigger } from "react-contextmenu";
import { ConnectedMenu, ConnectedGroupMenu } from "./ContextMenu.jsx";
import AddUsergroup from "./AddUsergroup.jsx";
import ChangeIcon from "./ChangeIcon.jsx";
import AddContent from "./AddContent.jsx";
class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      siteUrl: config.default.HTTPS
        ? `https://${config.default.host}:${config.default.port}`
        : `http://${config.default.host}:${config.default.port}`,
      currentDepth: 0,
      data: [],
      currentPath: [],
      currentDirId: [],
      editModeOn: false,
      currentUsergroupName: "",
      is_note: null,
      note: null,
      infoVisible: false,
      token: null,
      idToChangeIcon: null
    };
    this.getToken();
  }

  handleClick = (e, data) => {
    if (data.action === "Open") {
      this.openNote(data.name.slice(4));
    } else if (data.action === "Properties") {
      this.infoNote(data.is_note, data.name.slice(4));
    } else if (data.action === "Delete") {
      this.preDeleteNote(data.name.slice(4));
    }
  };

  handleClickGroup = (e, data) => {
    if (data.action === "Properties") {
      this.infoNote(data.is_note, data.name);
    } else if (data.action === "Delete") {
      this.preDeleteFolder(data.name);
    } else if (data.action === "Change icon") {
      this.preChangeIcon(data.name);
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

  getToken = () => {
    const that = this;
    if (!this.state.token) {
      fetch(`${this.state.siteUrl}/api/?query={getToken}`)
        .then(response => response.json())
        .then(res => res.data.getToken)
        .then(token =>
          that.setState({
            token: token
          })
        );
    }
  };

  getUsergroupRoot = usergroupId => {
    const that = this;
    fetch(
      `${
        this.state.siteUrl
      }/api/?query={getRootId(id_usergroup:${usergroupId},access_token:"${
        this.state.token
      }")}`
    )
      .then(response => response.json())
      .then(myJson => Number(myJson.data.getRootId))
      .then(rootId => {
        that.setState({
          currentDirId: [rootId]
        });
        that.updateContent(rootId);
      });
  };

  getContent(dir_id) {
    return fetch(
      `${
        this.state.siteUrl
      }/api/?query={getContent(id_notegroup:${dir_id},access_token:"${
        this.state.token
      }")}`
    )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .catch(error => console.error(error));
  }

  openNote = e => {
    let id = e;
    if (isNaN(e)) {
      id = e.target.id.slice(4);
    }
    window.open(`${this.state.siteUrl}/download/${id}`);
    return Number(id);
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
  };

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
              // Start note loop
              <ContextMenuTrigger
                id="DYNAMIC"
                holdToDisplay={1000}
                name={value.key}
                is_note={value.is_note}
                onItemClick={this.handleClick}
                collect={props => props}
                key={value.key}
              >
                <div className={style.elementWrapper} key={value.key}>
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
                        <i
                          onClick={this.preDeleteNote}
                          className="fas fa-times"
                        />
                      ) : null}
                    </div>
                  </div>
                </div>
              </ContextMenuTrigger>
            );
          } else {
            // Start usergroup loop
            content.push(
              <ContextMenuTrigger
                id="NOTEGROUP"
                holdToDisplay={1000}
                name={value.key}
                is_note={value.is_note}
                onItemClick={this.handleClickGroup}
                collect={props => props}
                key={value.key}
              >
                <div className={style.elementWrapper} key={value.key}>
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
                  </div>
                </div>
              </ContextMenuTrigger>
            );
          }
        }
        return content;
      }
    } else {
      return (
        <React.Fragment>
          <p className={style.no_group_chosen}>Wybierz grupę aby kontynuować</p>
          <div align="center">
            <AddUsergroup that={this} />
          </div>
        </React.Fragment>
      );
    }
  };

  changeMode = e => {
    e.preventDefault();
    this.setState(prevState => ({
      editModeOn: !prevState.editModeOn
    }));
  };

  preDeleteNote = e => {
    let note;
    if (isNaN(e)) {
      note = e.target.parentElement.previousSibling.id.slice(4);
    } else {
      note = e;
    }
    this.setState({
      noteToDelete: Number(note)
    });
    return Number(note);
  };

  preDeleteFolder = e => {
    let folder;
    if (isNaN(e)) {
      folder = e.target.parentElement.previousSibling.id;
    } else {
      folder = e;
    }
    this.setState({
      folderToDelete: Number(folder)
    });
    return Number(folder);
  };

  preChangeIcon = id => {
    this.setState({
      idToChangeIcon: id
    });
  };

  updateContent = () => {
    const that = this;
    setTimeout(() => {
      this.getContent(this.state.currentDirId[this.state.currentDepth]).then(
        innerJson => {
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
        }
      );
    }, 100);
  };

  updateCurrentUsergroup = e => {
    this.getUsergroupRoot(e.target.id);
    let usergroupName = e.target.innerText;
    let usergroupId = e.target.id;
    this.setState({
      currentDepth: 0,
      currentDirId: [],
      currentPath: [],
      currentUsergroupName: usergroupName,
      currentUsergroupId: usergroupId,
      note: null
    });
  };

  listOfUsers = () => {
    return (
      <div>
        <ListOfUsers
          usergroup={this.state.currentUsergroupId}
          siteUrl={this.state.siteUrl}
          token={this.state.token}
        />
      </div>
    );
  };

  render() {
    return (
      <React.Fragment>
        <UsergroupList
          updateUsergroup={this.updateCurrentUsergroup}
          siteUrl={this.state.siteUrl}
          token={this.state.token}
        />
        <button
          className="menu-toggler"
          onClick={() => {
            if (
              !document.getElementById("sidebar").classList.contains("navOpen")
            ) {
              document
                .getElementById("sidebar")
                .animate([{ left: "-70vw" }, { left: "0" }], {
                  duration: 300
                });
              document
                .querySelector("nav")
                .animate([{ left: "-70vw" }, { left: "0" }], {
                  duration: 300
                });
              document.getElementById("sidebar").classList.add("navOpen");
              document.querySelector("nav").classList.add("navOpen");
            }
          }}
        >
          <i className="fas fa-bars" />
        </button>
        <AddUsergroup that={this} />
        <div className={style.mainContent}>
          <p className={style.usergroupName}>
            {this.state.currentUsergroupName}
          </p>
          <div className={style.actionBar} key="actionBar">
            {this.state.currentUsergroupName ? <AddContent that={this} /> : ""}
            {this.state.currentUsergroupId ? this.listOfUsers() : ""}
            {this.state.currentUsergroupName ? (
              <EditMode
                changeMode={this.changeMode}
                isOn={this.state.editModeOn}
              />
            ) : (
              ""
            )}
          </div>
          <ConfirmDelete that={this} />
          <ChangeIcon that={this} />
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
            token={this.state.token}
          />
          <ConnectedMenu />
          <ConnectedGroupMenu />
        </div>
      </React.Fragment>
    );
  }
}

export default Notatki;
