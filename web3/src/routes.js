import React from 'react';
import Home from './components/homePage';
import NotFoundPage from './components/notFoundPage';
import { Switch, Route } from 'react-router-dom';

var Routes = () => (
  <Switch>
    <Route exact path="/" name="app" component={Home} />
    <Route name="home" path="/home" component={Home} />
    <Route component={NotFoundPage} />
  </Switch>
);

export default Routes;

// <Route name="authors" handler={require('./components/authors/authorPage')} />
// <Route name="addAuthor" path="author" handler={require('./components/authors/manageAuthorPage')} />
// <Route name="manageAuthor" path="author/:id" handler={require('./components/authors/manageAuthorPage')} />
//
// <Route name="courses" handler={require('./components/courses/coursePage')} />
// <Route name="addCourse" path="course" handler={require('./components/courses/manageCoursePage')} />
// <Route name="manageCourse" path="course/:id" handler={require('./components/courses/manageCoursePage')} />
//
// <Route name="about" handler={require('./components/about/aboutPage')} />


// <Redirect from="about-us" to="about" />
// <Redirect from="awthurs" to="authors" />
// <Redirect from="about/*" to="about" />
