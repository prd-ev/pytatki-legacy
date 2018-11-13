import React from "react";
import style from "../scss/Modal.scss";

export default class Modal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false
    };
    this.close = this.close.bind(this);
  }

  close(e) {
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
    this.setState({
      visible: false
    });
  }

  render() {
    return (
      <React.Fragment>
        <button
          type="button"
          onClick={() => {
            if (!this.state.visible) {
              if (this.props.action) this.props.action();
              this.setState({ visible: true });
            }
          }}
          className="btn bar"
        >
          {this.props.name}
        </button>
        {this.state.visible ? (
          <div className={style.modal_view} onClick={this.close}>
            <div
              className={style.modal}
              onClick={e => {
                e.cancelBubble = true;
                if (e.stopPropagation) e.stopPropagation();
              }}
            >
              <a className={style.close} onClick={this.close}>
                <i className="fas fa-times" />
              </a>
              {this.props.children}
            </div>
          </div>
        ) : null}
      </React.Fragment>
    );
  }
}
