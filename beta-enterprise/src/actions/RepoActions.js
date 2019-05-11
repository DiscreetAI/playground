import Reflux from 'reflux';

var RepoActions = Reflux.createActions({
  fetchRepoData: {children: ['completed', 'failed'], asyncResult: true},
  fetchCoordinatorStatus: {children: ['completed', 'failed'], asyncResult: true},
  fetchLogs: {children: ['completed', 'failed'], asyncResult: true},
});

export default RepoActions;
