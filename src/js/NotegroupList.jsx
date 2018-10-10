import React from 'react'
import styles from "../scss/test.scss";

const getUsergroups = () => {
  fetch(siteUrl + '/api?query={getUsergroupsOfUser}')
    .then(response => response.json())
    .then(myJson => JSON.parse(myJson.data.getContent))
    .then(function (innerJson) {
      let usergroups = [];
      for (const usergroup of innerJson) {
        let object = {};
        object["key"] = usergroup.idusergroup;
        object["name"] = usergroup.name;
        usegroups.push(object);
      };
      return usergroups
    })
    .catch(error => console.log(error));
}


const NotegroupList = () => {
  return (
    <div className={styles.lala}>
      NotegroupList
        {getUsergroups()}
    </div>
  )
}

export default NotegroupList