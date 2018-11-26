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
        return innerJson.map(usergroup => ({
          key: usergroup.idusergroup,
          name: usergroup.name,
          color: usergroup.color,
          imagePath: usergroup.image_path
        }));
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
