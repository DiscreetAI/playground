import Reflux from 'reflux';

var RepoDataActions = Reflux.createActions({
  fetchRepoData: {children: ['completed', 'failed'], asyncResult: true},
  fetchCoordinatorStatus: {children: ['completed', 'failed'], asyncResult: true},
  fetchLogs: {children: ['completed', 'failed'], asyncResult: true},
});

export default RepoDataActions;
