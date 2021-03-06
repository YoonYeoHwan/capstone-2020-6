import React from 'react';
import './Router.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';

// for Pages
import PageMain from './pages/PageMain';
import PageLogin from './pages/PageLogin';
import PageRegister from './pages/PageRegister';
import PageAbout from './pages/PageAbout';
import PageMypage from './pages/PageMypage';
import PageLabelingImgSelect from './pages/PageLabelingImgSelect';
import PageMypagePW from './pages/PageMypagePW';
import PageLabelingRegister from './pages/PageLabelingRegister';
import PagePoints from './pages/PagePoints';
import PageLabelingRequesterResult from './pages/PageLabelingRequesterResult';
import PageLabeling from './pages/PageLabeling';
import PageLabelingTextWrite from './pages/PageLabelingTextWrite';
import PageLabelingTextSelect from './pages/PageLabelingTextSelect';
import PageLabelingImageCapture from './pages/PageLabelingImageCapture';
import PageMypageProject from './pages/PageMypageProject';
import PageCaptcha from './pages/PageCaptcha';
import PageViewAllProjects from './pages/PageViewAllProjects';
import PageViewAllProjectsFinished from './pages/PageViewAllProjectsFinished';
import PageLabelingSetting from './pages/PageViewAllProjectsFinished';
import PageLabelingTextSelectByImage from './pages/PageLabelingTextSelectByImage';
import PageLabelingParticipantsResult from './pages/PageLabelingParticipantsResult';

// for Components
import Navigation from './components/Navigation';
import Footer from './components/Footer';

// for Mobx
import {inject, observer} from 'mobx-react';
import MenuStore from './stores/MenuStore';
// import {useCookies} from 'react-cookie';
// import {instanceOf} from 'prop-types';
// import {withCookies, Cookies} from 'react-cookie';

export interface Props {
    menuStore?: MenuStore
}

@inject('menuStore') @observer
class App extends React.Component<Props> {
  render() {
    return (
      <Router>
        <Navigation />
        <Switch>
          <Route path='/about'>
            <PageAbout />
          </Route>
          <Route path='/captcha'>
            <PageCaptcha/>
          </Route>
          <Route path="/login">
            <PageLogin />
          </Route>
          <Route path='/allprojects'>
            <PageViewAllProjects/>
          </Route>
          <Route path='/allProjectsFinished'>
            <PageViewAllProjectsFinished/>
          </Route>
          <Route exact path='/mypage'>
            <PageMypage/>
          </Route>
          <Route path='/mypage/points'>
            <PagePoints/>
          </Route>
          <Route path='/mypage/projects'>
            <PageMypageProject/>
          </Route>
          <Route path='/mypage/pw'>
            <PageMypagePW/>
          </Route>
          <Route path='/register'>
            <PageRegister/>
          </Route>
          <Route path='/setting/:postId'>
            <PageLabelingSetting/>
          </Route>
          <Route path='/labeling/:postId/0/:dataId'>
            <PageLabelingTextWrite/>
          </Route>
          <Route path="/labeling/:postId/1/:dataId">
            <PageLabelingTextSelect/>
          </Route>
          <Route path="/labeling/:postId/2/:dataId">
            <PageLabelingImgSelect/>
          </Route>
          <Route path='/labeling/:postId/3/:dataId'>
            <PageLabelingImageCapture/>
          </Route>
          <Route path='/labeling/:postId/4/:dataId'>
            <PageLabelingTextSelectByImage/>
          </Route>
          <Route path='/labeling/:postId/requesterResult'>
            <PageLabelingRequesterResult/>
          </Route>
          <Route path='/labeling/:postId/participantsResult'>
            <PageLabelingParticipantsResult/>
          </Route>
          <Route path='/labeling/:postId'>
            <PageLabeling/>
          </Route>
          <Route path='/labelingRegister'>
            <PageLabelingRegister/>
          </Route>
          <Route path='/'>
            <PageMain />
          </Route>
        </Switch>
        <Footer/>
      </Router>
    );
  }
}

export default App;
