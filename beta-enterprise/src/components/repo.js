import React, { Component } from 'react';
import NotFoundPage from './notFoundPage';
import { Link } from 'react-router-dom';

class Repo extends Component {

  state = {
    repoWasFound: false,
    repoData: {},
    repoStatus: {},
    repoLogs: [],
  }

  componentDidMount() {
    const { match: { params } } = this.props;
    const repoId = params.repoId;

    // TODO: Get repo data using the repoId.

    this.setState({
      repoWasFound: true,
      repoData: {
        'Id': 1,
        'RepoName': 'username/repo1',
        'Description': 'A repo used to test things out. There\'s nothing here and never will. Well, maybe.',
        'CreatedAt': 1546344000,
        'ExploratoryData': {},
      },
      repoStatus: {
        'Busy': false,
      },
      repoLogs: [
        {
          "Content": "{\"session_id\": \"e395a34e-c26a-47de-83c5-441e71f6cd58\", \"round\": 1, \"action\": \"TRAIN\", \"weights\": \"omitted\", \"omega\": 0.5130145837179251}",
          "ContentType": "ROUND_COMPLETED",
          "Id": "1ccd263e-c8ca-46ac-b776-3a9f74b3504b",
          "RepoId": "testing_id",
          "SessionId": "e395a34e-c26a-47de-83c5-441e71f6cd58",
          "Timestamp": 1555407592,
          "WeightsS3Key": "s3://updatestore/test/e395a34e-c26a-47de-83c5-441e71f6cd58/2/model.h5"
        },
        {
          "Content": "{\"session_id\": \"e395a34e-c26a-47de-83c5-441e71f6cd58\", \"round\": 2, \"action\": \"TRAIN\", \"weights\": \"omitted\", \"omega\": 0.7098024736939266}",
          "ContentType": "ROUND_COMPLETED",
          "Id": "0b34d1d3-c9e1-42b4-9965-394bd5a8a345",
          "RepoId": "testing_id",
          "SessionId": "e395a34e-c26a-47de-83c5-441e71f6cd58",
          "Timestamp": 1555407612,
          "WeightsS3Key": "s3://updatestore/test/e395a34e-c26a-47de-83c5-441e71f6cd58/3/model.h5"
        }
      ]
    })
  }

  render() {
    if (!this.state.repoWasFound) {
      return <NotFoundPage />
    }

    return (
      <div>
        <div className="row">
          <div className="col-1"></div>
          <div className="col-8">
            <h3>{this.state.repoData.RepoName}</h3>
            <p>{this.state.repoData.Description}</p>
          </div>
          <div className="col-2 text-right">
            {this.state.repoStatus.Busy ? (
              <span className="badge badge-pill badge-light">Working...</span>
            ) : (
              <span className="badge badge-pill badge-dark">Idle</span>
            )}

            <p className="mt-3"><Link to="/explora" className="btn btn-xs btn-light"><b>Open Explora</b></Link></p>
          </div>
        </div>

        <div className="row mt-5">
          <div className="col-1"></div>
          <div className="col-10">
            <div className="card bg-dark">
              <div className="card-header">
                <h5>Exploratory Data (ED)</h5>
                <p className="mb-0"><small>Example data that each client should be storing locally. The models sent should be able to train on this structure.</small></p>
              </div>
              <div className="card-body text-center mt-3">
                <p className="card-text"><b>No exploratory data yet.</b></p>
                <p><small>(Feature in development.)</small></p>
                <div className="row mt-4">
                  <div className="col-4"></div>
                  <div className="col-2 text-center">
                    <a href="#" className="btn btn-primary disabled">Upload ED</a>
                  </div>
                  <div className="col-2 text-center">
                    <Link to="/explora" className="btn btn-light">Explore ED</Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row mt-5">
          <div className="col-1"></div>
          <div className="col-10">
          <div className="card bg-dark">
            <div className="card-header">
              <h5>Model Hub</h5>
              <p className="mb-0"><small>Download or evaluate your resulting models from here.</small></p>
            </div>
            <div className="card-body text-center mt-3">
              <p className="card-text"><b>No model has been trained yet.</b></p>
              <Link to="/explora" className="btn btn-light mt-2">Train a new model</Link>
            </div>
          </div>
          </div>
        </div>

        <div className="row mt-5">
          <div className="col-1"></div>
          <div className="col-10">
          <div className="card bg-dark">
            <div className="card-header">
              <h5>Logs</h5>
              <p className="mb-0"><small>History of training sessions for this repo. You can debug your environment from here.</small></p>
            </div>
            <div className="card-body text-center mt-3">
              <p className="card-text"><b>No model has been trained yet.</b></p>
              <Link to="/explora" className="btn btn-light mt-2">Train a new model</Link>
            </div>
          </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Repo;
