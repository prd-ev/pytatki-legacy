import React, { Component } from 'react';
import ComponentStyle from '../scss/UsergroupList.scss'

export default class UsergroupList extends Component {
  constructor(props) {
    super(props)
    this.state = {
      usergroups: []
    }
    this.getUsergroups();
  }

  getUsergroups = () => {
    const siteUrl = this.props.siteUrl;
    const that = this;
    return fetch(siteUrl + '/api?query={getToken}')
      .then(response => response.json())
      .then(res => {
        if (/\d/.test(res.data.getToken)) {
          return res.data.getToken
        }
        alert(res.data.getToken);
      })
      .then(token => fetch(siteUrl + '/api?query={getUsergroups(access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getUsergroups))
      .then(function (innerJson) {
        let usergroups = [];
        for (const usergroup of innerJson) {
          let object = {};
          object["key"] = usergroup.idusergroup;
          object["name"] = usergroup.name;
          object["color"] = usergroup.color;
          object["imagePath"] = usergroup.image_path;
          usergroups.push(object);
        };
        return usergroups
      })
      .then(plainGroups => {
        let groups = []
        for (const group of plainGroups) {
          groups.push(<li onClick={this.props.updateUsergroup} key={group.key} id={group.key}>{group.name}</li>);
        }
        that.setState({
          usergroups: groups
        });
      })
      .catch(error => console.log(error));
  }

  render() {
    return (
      <div className={ComponentStyle.sidebar}>
        UsergroupList
        <ul>
          {this.state.usergroups}
        </ul>
      </div>
    )
  }
}