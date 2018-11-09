import React from "react";

export default class ListOfUsers extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      users: null
    };
    this.fetchUsers();
  }

  fetchUsers() {
    const siteUrl = this.props.siteUrl;
    return fetch(siteUrl + "/api/?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            `/api?query={getMembers(id_usergroup: ${
              this.props.usergroup
            }, access_token:"${token}")}`
        )
      )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getMembers))
      .then(data => this.setState({ users: data }));
  }

  render() {
    return <div>Users</div>;
  }
}
