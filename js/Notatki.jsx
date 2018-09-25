import React from "react";
import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      subjects: null,
      current_subject: null,
      current_topic: null
    };
  }

  componentWillMount() {
      var xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
      if (xhttp.status === 200) {
        this.setState({subjects: xhttp.responseText});
      }
      return 0;
    }.bind(this);
    xhttp.open('GET', 'http://127.0.0.1:5000/graphql?query={getRootFolders(id_usergroup:1,id_user:1)}');
    xhttp.send();
  }


  updateNotes = updated_notes => {
    this.setState((prevState, props) => ({ notatki: updated_notes }));
  };

  changeCurrentSubject = e => {
    this.setState({ current_subject: e.target.className, current_topic: null });
  };

  changeCurrentTopic = e => {
    this.setState({ current_topic: e.target.className });
  };

  packSubjects = () => {
    if (this.state.subjects) {
      var subjects = [];
      for (let value of this.state.subjects) {
        subjects.push(<h1 className={value} onClick={this.changeCurrentSubject} key={value}>
          {value}
        </h1>);
      }
      return subjects;
    }
    return 0;
  };

  packTopics = () => {
    if (this.state.notatki) {
      let topics = [];
      for (let value of topics_temp) {
        topics.push(<h2 className={value} onClick={this.changeCurrentTopic} key={value}>
          {value}
        </h2>);
      }
      return topics;
    }
    return 0;
  };

  packNotes = () => {
    if (this.state.notatki) {
      let notatki = [];
      for (let value of this.state.notatki) {
        notatki.push(<h3 className={value} onClick={this.changeCurrentTopic} key={value}>
          {value}
        </h3>);
      }
      return notatki;
    }
    return 0;
  };

  render() {
    return (<div>
      <AddNote notatki={this.state.notatki} update={this.updateNotes} /> {this.packSubjects()}
      {this.packTopics()}
      {this.packNotes()}
    </div>);
  }
}

export default Notatki;
