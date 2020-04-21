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
import PageLabelingResult from './pages/PageLabelingResult';
import PageLabeling from './pages/PageLabeling';
import PageLabelingTextWrite from './pages/PageLabelingTextWrite';
import PageLabelingTextButton from './pages/PageLabelingTextButton';
import PageLabelingImageCapture from './pages/PageLabelingImageCapture';

// for Components
import Navigation from './components/Navigation';
import Footer from './components/Footer';

// for Mobx
import {inject, observer} from 'mobx-react';
import MenuStore from './stores/MenuStore';
import {useCookies} from 'react-cookie';
import {instanceOf} from 'prop-types';
import {withCookies, Cookies} from 'react-cookie';

export interface Props {
    menuStore?: MenuStore
}

@inject('menuStore') @observer
class App extends React.Component<Props> {

  constructor(props: any) {
    super(props);
  }
  render() {
    return (
      <Router>
        <Navigation />
        <Switch>
          <Route path='/about'>
            <PageAbout />
          </Route>
          <Route path="/login">
            <PageLogin />
          </Route>
          <Route exact path='/mypage'>
            <PageMypage/>
          </Route>
          <Route path='/mypage/points'>
            <PagePoints/>
          </Route>
          <Route path='/mypage/pw'>
            <PageMypagePW/>
          </Route>
          <Route path='/register'>
            <PageRegister/>
          </Route>
          <Route path='/labeling/imgcap'>
            <PageLabelingImageCapture/>
          </Route>
          <Route path="/labeling/:postid/imgsel">
            <PageLabelingImgSelect/>
          </Route>
          <Route path="/labeling/txtsel">
            <PageLabelingTextButton/>
          </Route>
          <Route path='/labeling/txtwrite'>
            <PageLabelingTextWrite/>
          </Route>
          <Route path='/labeling/result'>
            <PageLabelingResult/>
          </Route>
          <Route path='/labeling/:postid'>
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