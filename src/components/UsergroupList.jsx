import React from "react";
import style from "../scss/UsergroupList.scss";

export default class UsergroupList extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      usergroups: []
    };
    this.getUsergroups();
  }

  getUsergroups = () => {
    const siteUrl = this.props.siteUrl;
    return fetch(siteUrl + "/api/?query={getToken}")
      .then(response => response.json())
      .then(res => {
        if (/\d/.test(res.data.getToken)) {
          return res.data.getToken;
        }
        alert(res.data.getToken);
      })
      .then(token =>
        fetch(`${siteUrl}/api/?query={getUsergroups(access_token:"${token}")}`)
      )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getUsergroups))
      .then(innerJson => {
        let usergroups = [];
        innerJson.map(usergroup => {
          let object = {}; // new usergroup object
          object["key"] = usergroup.idusergroup;
          object["name"] = usergroup.name;
          object["color"] = usergroup.color;
          object["imagePath"] = usergroup.image_path;
          usergroups.push(object);
        });
        return usergroups; // array of all usergroups
      })
      .then(groups => {
        this.setState({
          usergroups: groups
        });
      })
      .catch(error => console.error(error));
  };

  render() {
    return (
      <div id="sidebar" className={style.sidebar}>
        <p>Klasy</p>
        <ul>
          {this.state.usergroups ? (
            this.state.usergroups.map(group => {
              return (
                <li key={group.key}>
                  <button
                    className="btn"
                    onClick={this.props.updateUsergroup}
                    id={group.key}
                  >
                    {group.name}
                  </button>
                </li>
              );
            })
          ) : (
            <i className="ld ld-ring ld-cycle" />
          )}
        </ul>
      </div>
    );
  }
}
