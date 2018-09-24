import React from "react";
import data from "../static/notatki.json";
import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      notatki: data,
      subjects: null,
      current_subject: null,
      current_topic: null
    };
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
    let subjects = [];
    let subjects_temp = [];
    for (let temp_value of this.state.notatki) {
      if (temp_value != null) {
        if (subjects_temp.indexOf(temp_value.substring(temp_value.indexOf("/") + 1, temp_value.indexOf("/", 1))) < 0) {
          subjects_temp.push(temp_value.substring(temp_value.indexOf("/") + 1, temp_value.indexOf("/", 1)));
        }
      }
    }
    for (let value of subjects_temp) {
      subjects.push(<h1 className={value} onClick={this.changeCurrentSubject} key={value}>
        {value}
      </h1>);
    }
    return subjects;
  };

  packTopics = () => {
    let topics_temp = [];
    let topics = [];
    for (let temp_value of this.state.notatki) {
      if (temp_value != null) {
        if (topics_temp.indexOf(temp_value.substring(temp_value.indexOf("/", 1) + 1, temp_value.lastIndexOf("/"))) < 0 && temp_value.substring(temp_value.indexOf("/") + 1, temp_value.indexOf("/", 1)) === this.state.current_subject) {
          topics_temp.push(temp_value.substring(temp_value.indexOf("/", 1) + 1, temp_value.lastIndexOf("/")));
        }
      }
    }
    for (let value of topics_temp) {
      topics.push(<h2 className={value} onClick={this.changeCurrentTopic} key={value}>
        {value}
      </h2>);
    }
    return topics;
  };

  packNotes = () => {
    let notatki = [];
    for (let value of this.state.notatki) {
      if (value != null) {
        if (value.substring(value.indexOf("/", 1) + 1, value.lastIndexOf("/")) === this.state.current_topic) {
          notatki.push(<h3 key={value}>{value.substring(value.lastIndexOf("/") + 1)}</h3>);
        }
      }
    }
    return notatki;
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
