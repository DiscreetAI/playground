import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import AuthStore from './../stores/AuthStore';

class NewRepo extends Component {

  constructor(props) {
    super(props);
    this.store = AuthStore;
  }

  render() {
    // Get number of repos left.
    // let reposLeft = this.state.claims["reposLeft"];
    let reposLeft = 1;

    if (reposLeft <= 0) {
      return (
        <div className="text-center">
          <h3>Sorry, but you have no more repos left.</h3>
          <p className="mt-4">If you want to upgrade your account to support more repos, <a href="#">please click here</a>.</p>
          <p className="mt-3"><Link to="/">Back to dashboard</Link></p>
        </div>
      );
    } else {
      return (
        <div className="row">
          <div className="col-4"></div>
          <div className="col-4">
            <h3>Create a new repo</h3>
            <p className="mt-3">Create a new repository to start doing private federated learning. Only you will be able to see this repository's settings.</p>
            <form className="mt-4">
              <div className="form-group">
               <label htmlFor="repoNameInput">Repo name</label>
               <input type="text" className="form-control" id="repoNameInput" aria-describedby="repoName" placeholder="awesome-dml-experiment" />
               <small id="repoNameHelp" className="form-text text-muted">Use a repo name you haven't used yet. Make it catchy.</small>
              </div>
              <div className="form-group">
               <label htmlFor="repoDescriptionInput">Brief description</label>
               <input type="text" className="form-control" id="repoDescriptionInput" placeholder="To do magic on users' data without even seeing it." />
               <small id="repoDescriptionHelp" className="form-text text-muted">Anything will do. Use this to know which repo is which.</small>
              </div>
              <div className="text-center mt-5">
                <button type="submit" className="btn btn-lg btn-primary">Create Repo</button>
              </div>
            </form>
          </div>
        </div>
      );
    }
  }
}

export default NewRepo;
