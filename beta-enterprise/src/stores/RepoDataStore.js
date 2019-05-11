import Reflux from 'reflux';
import RepoDataActions from './../actions/RepoDataActions';
import AuthStore from './AuthStore';
import Endpoints from './../constants/endpoints.js';


class RepoDataStore extends Reflux.Store {

  constructor () {
    super();
    this.init();
    this.listenables = RepoDataActions;
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

  onFetchRepoData(repoId) {
    if (AuthStore.state.isAuthenticated) {
      let jwtString = AuthStore.state.jwt;

      this.state.loading = true;
      this._changed();

      fetch(
        Endpoints["dashboardFetchRepoData"] + repoId, {
          method: 'GET',
          headers: {
            'Content-Type':'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + jwtString,
          },
        }
      ).then(response => {
        this._handleResponse(response, RepoDataActions.fetchRepoData);
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


  onFetchRepoLogs(repoId) {
    if (AuthStore.state.isAuthenticated) {
      let jwtString = AuthStore.state.jwt;

      this.state.loading = true;
      this._changed();

      fetch(
        Endpoints["dashboardFetchRepoData"] + repoId, {
          method: 'GET',
          headers: {
            'Content-Type':'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + jwtString,
          },
        }
      ).then(response => {
        // this._handleResponse(response, RepoLogsActions.fetchRepoData);
      });
    }
  }

  _changed () {
    this.trigger(this.state);
  }

}

export default RepoDataStore;
