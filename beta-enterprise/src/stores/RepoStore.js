import Reflux from 'reflux';
import RepoActions from './../actions/RepoActions';
import AuthStore from './AuthStore';
import Endpoints from './../constants/endpoints.js';


class RepoStore extends Reflux.Store {

  constructor () {
    super();
    this.init();
    this.listenables = RepoActions;
  }

  init () {
    this.state = {
      loading: true,
      error: false,
      repoWasFound: false,
      repoData: {},
      repoStatus: {},
      repoLogs: [],
    };
  }

  onFetchRepoData(repo_id) {
    if (AuthStore.state.isAuthenticated) {
      let jwtString = AuthStore.state.jwt;

      this.state.loading = true;
      this._changed();

      fetch(
        Endpoints["dashboardFetchRepoData"] + repo_id, {
          method: 'GET',
          headers: {
            'Content-Type':'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + jwtString,
          },
        }
      ).then(response => {
        this._handleResponse(response, RepoActions.fetchRepoData);
      });
    }
  }

  _handleResponse(response, refluxAction) {
    response.json().then(serverResponse => {
      if (response.status === 200) {
        refluxAction.completed(serverResponse);
      } else {
        // TODO: Use error returned by server.
        refluxAction.failed(serverResponse);
      }
    });
  }

  onFetchRepoDataCompleted (repoData) {
    this.state.repoWasFound = true;
    this.state.repoData = repoData;
    this.state.loading = false;
    this._changed();
  }

  onFetchRepoDataFailed (errorObject) {
    this.state.repoWasFound = false;
    this.state.repoData = {};
    this.state.error = errorObject["message"];
    this.state.loading = false;
    this._changed();
  }

  _changed () {
    this.trigger(this.state);
  }

}

export default RepoStore;
