import React from "react";
import PropTypes from "prop-types";
import Modal from "./Modal.jsx";

export default class ListOfUsers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      id: null,
      users: null,
      link: null
    };
  }

  fetchData = () => {
    const siteUrl = this.props.siteUrl;
    if (this.state.id == this.props.usergroup) {
    } else {
      fetch(
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
              this.setState({
                link: link,
                users: data,
                id: this.props.usergroup
              })
            )
        );
    }
  };

  shouldComponentUpdate(nextState, nextProps) {
    if (this.props.usergroup != nextProps.usergroup) return true;
    if (this.props.usergroup != nextState.id) {
      return true;
    }
    return false;
  }

  componentDidUpdate(prevProps) {
    if (this.props.usergroup != prevProps.usergroup) {
      this.setState({ link: null, users: null, id: null });
    }
  }

  render() {
    return (
      <div>
        <Modal name="Lista uzytkowników" action={this.fetchData}>
          <React.Fragment>
            <div>
              <h5>Lista uzytkowników</h5>
            </div>
            <div>
              Zaproś nowych uzytkowników
              <br />
              {this.state.link ? (
                <React.Fragment>
                  <textarea
                    id="link"
                    value={this.state.link}
                    readOnly
                    onClick={() => {
                      document.getElementById("link").focus();
                      document.getElementById("link").select();
                    }}
                  />
                  <span
                    onClick={() => {
                      document.getElementById("link").focus();
                      document.getElementById("link").select();
                      document.execCommand("copy");
                    }}
                  >
                    Copy
                  </span>
                </React.Fragment>
              ) : (
                <i className="ld ld-ring ld-cycle" />
              )}
              <hr />
              <h5>Uzytkownicy</h5>
              <ul>
                {this.state.users ? (
                  this.state.users.map(user => (
                    <li key={user.iduser}>
                      <a href={`/user/${user.login}`}>{user.login}</a>
                    </li>
                  ))
                ) : (
                  <i className="ld ld-ring ld-cycle" />
                )}
              </ul>
            </div>
          </React.Fragment>
        </Modal>
      </div>
    );
  }
}

ListOfUsers.propTypes = {
  siteUrl: PropTypes.string,
  token: PropTypes.string,
  usergroup: PropTypes.string
};
