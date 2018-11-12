import React from "react";

export default class ListOfUsers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: null,
      users: null,
      link: null
    };
    this.fetchData();
  }

  fetchData() {
    const siteUrl = this.props.siteUrl;
    return fetch(
      siteUrl +
        `/api/?query={getMembers(id_usergroup: ${
          this.props.usergroup
        }, access_token:"${this.props.token}")}`
    )
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getMembers))
      .then(data =>
        fetch(
          siteUrl +
            `/api/?query={generateInvitationLink(id_usergroup: ${
              this.props.usergroup
            }, access_token:"${this.props.token}")}`
        )
          .then(response => response.json())
          .then(myJson => myJson.data.generateInvitationLink)
          .then(link =>
            this.setState({ link: link, users: data, id: this.props.usergroup })
          )
      );
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (this.state.link != nextState.link) {
      return true;
    }
    if (this.props.usergroup != nextProps.usergroup) {
      return true;
    }
    return false;
  }

  componentDidUpdate() {
    if (this.state.id != this.props.usergroup) this.fetchData();
  }

  render() {
    if (this.state.users && this.state.link) {
      return (
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Lista uzytkowników</h5>
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
            Zaproś nowych uzytkowników
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
            <hr />
            {this.state.users.map(user => (
              <p key={user.iduser}>{user.login}</p>
            ))}
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              data-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      );
    } else {
      return "";
    }
  }
}
