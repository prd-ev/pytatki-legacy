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
        //this.setState({ subjects: xhttp.responseText.split(" ") });
        console.log(xhttp.responseText);
      }
      this.setState({ subjects: ['Matematyka', 'Programowanie', 'To działa'] });//mock
      return 0;
    }.bind(this);
    xhttp.open('GET', 'http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:1,id_user:1)}');
    xhttp.send();
  }


  updateNotes = updated_notes => {
    this.setState((prevState, props) => ({ notatki: updated_notes }));
  };

  changeCurrentSubject = e => {
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
      if (xhttp.status === 200) {
        //this.setState({ topics: xhttp.responseText.split(",") });
        console.log(xhttp.responseText);
      }
      this.setState({ topics: ['Metafizyka', 'Sarmatyzm', 'Dworski'] });//mock
      return 0;
    }.bind(this);
    xhttp.open('GET', 'http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:1,id_user:1)}');
    xhttp.send();
    this.setState({ current_subject: e.target.className, current_topic: null, notes: null });
  };

  changeCurrentTopic = e => {
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
      if (xhttp.status === 200) {
        //this.setState({ notes: xhttp.responseText.split(" ") });
        console.log(xhttp.responseText);
      }
      this.setState({ notes: ['Notatka1', 'Notatka2', 'Notatka3'] });//mock
      return 0;
    }.bind(this);
    xhttp.open('GET', 'http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:1,id_user:1)}');
    xhttp.send();
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
    return null;
  };

  packTopics = () => {
    if (this.state.topics) {
      let topics = [];
      for (let value of this.state.topics) {
        topics.push(<h2 className={value} onClick={this.changeCurrentTopic} key={value}>
          {value}
        </h2>);
      }
      return topics;
    }
    return null;
  };

  packNotes = () => {
    if (this.state.notes) {
      let notatki = [];
      for (let value of this.state.notes) {
        notatki.push(<h3 className={value} onClick={this.changeCurrentTopic} key={value}>
          {value}
        </h3>);
      }
      return notatki;
    }
    return null;
  };

  render() {
    return (<div>
      <AddNote subjects={this.state.subjects} update={this.updateNotes} />
      {this.packSubjects()}
      {this.packTopics()}
      {this.packNotes()}
    </div>);
  };
}

export default Notatki;
