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
    fetch('http://127.0.0.1:5000/graphql?query={getRootId(id_usergroup:3,id_user:1)}')
      .then(response => response.json())
      .then(myJson => fetch('http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:' + JSON.stringify(myJson) + ',id_user:1)}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .then(function (innerJson) {
        let result = [];
        for (const notegroup of innerJson.childrens) {
          result.push(notegroup.name);
        };
        this.setState({ subjects: result });
      })
      .catch(error => console.log(error));
  }


  updateNotes = updated_notes => {
    this.setState((prevState, props) => ({ notatki: updated_notes }));
  };

  changeCurrentSubject = e => {
    fetch('http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:2,id_user:1)}')
      .then(function (response) {
        return response.json();
      })
      .then(function (myJson) {
        return JSON.parse(myJson.data.getContent);
      })
      .then(function (innerJson) {
        let result = [];
        for (const notegroup of innerJson.childrens) {
          result.push(notegroup.name);
        };
        this.setState({ subjects: result });
      });
  };

  changeCurrentTopic = e => {
    fetch('http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:2,id_user:1)}')
      .then(function (response) {
        return response.json();
      })
      .then(function (myJson) {
        return JSON.parse(myJson.data.getContent);
      })
      .then(function (innerJson) {
        let result = [];
        for (const notegroup of innerJson.childrens) {
          result.push(notegroup.name);
        };
        this.setState({ subjects: result });
      });
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
