import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class RepoModels extends Component {

  render() {
    let content;
    if (this.props.logs.length === 0) {
      content = (
        <div>
          <p className="card-text"><b>No model has been trained yet.</b></p>
          <Link to="/explora" className="btn btn-dark mt-2">Train a new model</Link>
        </div>
      );
    } else {
      content = (

        <table className="table text-left table-striped">
          <thead>
            <tr>
              <th scope="col">SessionId</th>
              <th scope="col">Round</th>
              <th scope="col">Time</th>
              <th scope="col">Evaluation Results</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>

            {this.props.logs.map((log, index) => {
              return <tr key={index}>
                <th scope="row">{log.SessionId}</th>
                <td>{JSON.parse(log.Content).round}</td>
                <td>{this._formatTime(log.Timestamp)}</td>
                <td>-</td>
                <td>
                  <a href="#evaluate-model" className="btn btn-xs btn-warning disabled">Evaluate Model</a>
                  <a href="#explore-model" className="btn btn-xs btn-dark ml-2">Explore Model</a>
                  <a href="#download-model" className="btn btn-xs btn-primary ml-2">Download Model</a>
                </td>
              </tr>
            })}
          </tbody>
        </table>
      );
    }

    return (
      <div className="row mt-5">
        <div className="col-1"></div>
        <div className="col-10">
        <div className="card">
          <div className="card-header">
            <h5>Model Hub</h5>
            <p className="mb-0"><small>Download or evaluate your resulting models from here.</small></p>
          </div>
          <div className="card-body text-center mt-3">
            {content}
          </div>
        </div>
        </div>
      </div>
    )
  }

  _formatTime(timestamp) {
    var t = new Date(timestamp * 1000);
    return t.toISOString();
  }
}

export default RepoModels;
