import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class RepoList extends Component {

  state = {
    repos: []
  }

  componentDidMount() {
    this.setState({
      repos: [
        {
          'uid': 1,
          'repoName': 'username/repo1'
        },
        {
          'uid': 2,
          'repoName': 'username/repo2'
        },
        {
          'uid': 3,
          'repoName': 'username/repo3'
        },
      ]
    })
  }
  render() {
    if (this.state.repos.length === 0) {
      return (
        <div>
           <h3 class="text-center">You don't own any repos yet.</h3>
           <p class="lead text-center mt-4">
             Start by creating <Link to="new" className="lead">a new repo.</Link>
           </p>
        </div>
      )
    }

    return (
      <div>
        {this.state.repos.map(function(repo, index) {
          return (
            <div class="jumbotron bg-dark" key={index}>
              <div class="row">
                <div class="col">
                  <h4><Link to={"repo/" + repo.uid} className="display-5 text-light">{repo.repoName}</Link></h4>
                </div>
                <div class="col text-right">
                  <Link to={"explora/" + repo.uid} className="lead text-secondary">Open Explora</Link>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    )
  }
}

export default RepoList;
