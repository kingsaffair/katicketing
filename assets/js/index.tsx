import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as injectTapEventPlugin from 'react-tap-event-plugin';

import {Main} from './Main';
import {Theme} from './Theme';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

ReactDOM.render(<Theme><Main /></Theme>, document.getElementById('app'));
