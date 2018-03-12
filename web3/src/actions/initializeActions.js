import Dispatcher from '../dispatcher/appDispatcher';
import ActionTypes from '../constants/actionTypes';

// var AuthorApi = require('../api/authorApi');
// var CourseApi = require('../api/courseApi');

var InitializeActions = {
  initApp: function() {

    Dispatcher.dispatch({
      actionType: ActionTypes.INITIALIZE,
      initialData: {
        // authors: AuthorApi.getAllAuthors(),
        // courses: CourseApi.getAllCourses()
      }
    });

  }
};

export default InitializeActions;
// module.exports = InitializeActions;
