import React, { Component } from 'react'
import styles from "../scss/test.scss";

export default class NotegroupList extends Component {
  render() {
    constructor(props) {
      super(props)
      this.state = {

      }
      const that = this;
      fetch(siteUrl + '/api?query={getUsergroupsOfUser}')
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
        })
        .catch(error => console.log(error));
    }



    //fetch wszystkich notegroup dla użytkownika
    //spakowanie wyników w listę

    return (
      <div className={styles.lala}>
        NotegroupList
        {/*wyświetlenie listy*/}
      </div>
    )
  }
}
