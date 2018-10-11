import React from 'react'

const siteUrl = "http://127.0.0.1:5000"

const getUsergroups = () => {
  fetch(siteUrl + '/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch(siteUrl + '/api?query={getUsergroups(access_token:"' + token + '")}'))
      .then(response => console.log(response.json()))
      .then(myJson => JSON.parse(myJson.data.getUsergroups))
      .then(function (innerJson) {
      let usergroups = [];
      for (const usergroup of innerJson) {
        let object = {};
        object["key"] = usergroup.idusergroup;
        object["name"] = usergroup.name;
        object["color"] = usergroup.color;
        object["imagePath"] = usergroup.image_path;
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