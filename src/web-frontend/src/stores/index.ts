import NavigationStore from './NavigationStore';
import MenuStore from './MenuStore';
import ProjectListStore from './ProjectListStore';
import LoginStore from './loginStore';
import LabelingTextButtonStore from './LabelingTextButtonStore';
import LabelingImgStore from './LabelingImgStore';
import LabelingPageStore from './LabelingPageStore';
import MyPageListStore from './MyPageListStore';
import LabelingPageTextWrite from './LabelingTextWriteStore';

export default {
  navigationStore: new NavigationStore(),
  menuStore: new MenuStore(),
  projectListStore: new ProjectListStore(),
  loginStore: new LoginStore(),
  labelingTextButtonStore: new LabelingTextButtonStore(),
  labelingImgStore: new LabelingImgStore(),
  labelingPageStore: new LabelingPageStore(),
  myPageListStore: new MyPageListStore(),
  labelingTextWriteStore: new LabelingPageTextWrite(),
};