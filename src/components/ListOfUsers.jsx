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
    this.invitationLink();
    return fetch(siteUrl + "/api/?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            `/api/?query={getMembers(id_usergroup: ${
              this.props.usergroup
            }, access_token:"${token}")}`
        )
      )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getMembers))
      .then(data => this.setState({ users: data }));
  }

  invitationLink = () => {
    const siteUrl = this.props.siteUrl;
    return fetch(siteUrl + "/api/?query={getToken}")
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token =>
        fetch(
          siteUrl +
            `/api/?query={generateInvitationLink(id_usergroup: ${
              this.props.usergroup
            }, access_token:"${token}")}`
        )
      )
      .then(response => response.json())
      .then(myJson => myJson.data.generateInvitationLink)
      .then(data => this.setState({ link: data }));
  };

  render() {
    if (this.state.users && this.state.link) {
      return (
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Lista uzytkowników</h5>
            <br />
            <textarea
              id="link"
              value={this.state.link}
              readOnly
              onClick={() => {
                document.getElementById("link").focus();
                document.getElementById("link").select();
              }}
            />
            <button
              onClick={() => {
                document.getElementById("link").focus();
                document.getElementById("link").select();
                document.execCommand("copy");
              }}
            >
              Copy
            </button>
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">
            {this.state.users.map(user => (
              <p key={user.iduser}>{user.login}</p>
            ))}
          </div>
        </div>
      );
    } else {
      return "";
    }
  }
}
