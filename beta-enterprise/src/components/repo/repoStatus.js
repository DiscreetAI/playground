import React, { Component } from 'react';

class RepoStatus extends Component {
  render() {
    const isBusy = this.props.isBusy;
    if (isBusy) {
      return <span className="badge badge-pill badge-light">Working...</span>
    } else {
      return <span className="badge badge-pill badge-secondary">Idle</span>;
    }
  }
}

export default RepoStatus;
