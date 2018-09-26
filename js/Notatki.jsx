import React from "react";
import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      subjects: null,
      topics: null,
    };
  }

  componentWillMount() {
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getRootId(id_usergroup:3,access_token:"' + token + '")}')
        .then(response => response.json())
        .then(myJson => (myJson.data.getRootId))
        .then(myJson => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + Number(myJson) + ',access_token:"' + token + '")}'))
        .then(response => response.json())
        .then(myJson => JSON.parse(myJson.data.getContent))
      )
      .then(function (innerJson) {
        let result = [];
        for (let notegroup of innerJson) {
          let object = {};
          object["title"] = notegroup.title;
          if (notegroup.idnote) {
            object["key"] = notegroup.idnote;
          } else {
            object["key"] = notegroup.idnotegroup;
          }
          result.push(object);
        };
        that.setState({ subjects: result });
      })
      .catch(error => console.log(error));
  }


  updateNotes = updated_notes => {
    this.setState((prevState, props) => ({ notatki: updated_notes }));
  };

  changeCurrentSubject = e => {
    let selected_subject = e.target.id;
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + selected_subject + ',access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .then(function (innerJson) {
        let result = [];
        for (let notegroup of innerJson) {
          let object = {};
          object["title"] = notegroup.title;
          if (notegroup.idnote) {
            object["key"] = notegroup.idnote;
          } else {
            object["key"] = notegroup.idnotegroup;
          }
          result.push(object);
        };
        that.setState({ topics: result });
      })
      .catch(error => console.log(error));
  };

  changeCurrentTopic = e => {
    let selected_topic = e.target.id;
    const that = this;
    fetch('http://127.0.0.1:5000/api?query={getToken}')
      .then(response => response.json())
      .then(res => res.data.getToken)
      .then(token => fetch('http://127.0.0.1:5000/api?query={getContent(id_notegroup:' + selected_topic + ',access_token:"' + token + '")}'))
      .then(response => response.json())
      .then(myJson => JSON.parse(myJson.data.getContent))
      .then(function (innerJson) {
        let result = [];
        for (let notegroup of innerJson) {
          let object = {};
          object["title"] = notegroup.title;
          if (notegroup.idnote) {
            object["key"] = notegroup.idnote;
          } else {
            object["key"] = notegroup.idnotegroup;
          }
          result.push(object);
        };
        that.setState({ topics: result });
      })
      .catch(error => console.log(error));
  };

  packSubjects = () => {
    if (this.state.subjects) {
      var subjects = [];
      for (let value of this.state.subjects) {
        subjects.push(<h1 onClick={this.changeCurrentSubject} id={value.key} key={value.key}>
          {value.title}
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
        topics.push(<h2 onClick={this.changeCurrentTopic} id={value.key} key={value.key}>
          {value.title}
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
        notatki.push(<h3 onClick={this.changeCurrentTopic} key={value}>
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
