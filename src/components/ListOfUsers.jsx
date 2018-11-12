import React from "react";
import style from "../scss/ListOfUsers.scss";
import PropTypes from "prop-types";

export default class ListOfUsers extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      id: null,
      users: null,
      link: null
    };
  }

  fetchData = () => {
    const siteUrl = this.props.siteUrl;
    if (this.state.id == this.props.usergroup) {
      this.setState({ visible: true });
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
                id: this.props.usergroup,
                visible: true
              })
            )
        );
    }
  };

  shouldComponentUpdate(nextState) {
    if (this.state.visible != nextState.visible) return true;
    if (this.state.link != nextState.link) {
      return true;
    }
    return false;
  }

  modal() {
    if (this.state.visible) {
      return (
        <div className={style.modal}>
          <div>
            <h5>Lista uzytkowników</h5>
          </div>
          <div>
            Zaproś nowych uzytkowników
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
            <span
              onClick={() => {
                document.getElementById("link").focus();
                document.getElementById("link").select();
                document.execCommand("copy");
              }}
            >
              Copy
            </span>
            <hr />
            <h5>Uzytkownicy</h5>
            <ul>
              {this.state.users.map(user => (
                <li key={user.iduser}>{user.login}</li>
              ))}
            </ul>
          </div>
          <span
            onClick={() => {
              this.setState({ visible: false });
            }}
          >
            Close
          </span>
        </div>
      );
    }
  }

  render() {
    return (
      <React.Fragment>
        <button
          type="button"
          onClick={() => {
            if (!this.state.visible) this.fetchData();
          }}
          className="btn bar"
        >
          Lista uzytkowników
        </button>
        {this.modal()}
      </React.Fragment>
    );
  }
}

ListOfUsers.propTypes = {
  siteUrl: PropTypes.string,
  token: PropTypes.string,
  usergroup: PropTypes.string
};
