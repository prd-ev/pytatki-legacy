import React from 'react'

const siteUrl = "127.0.0.1:5000"

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
    <div>
      NotegroupList
        {getUsergroups()}
    </div>
  )
}

export default NotegroupList