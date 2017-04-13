import * as React from 'react';
import {BrowserRouter as Router, Route, Link} from 'react-router-dom'

import {AdminDrawer} from './AdminDrawer';
import {ListView} from './ListView';
import {DetailView} from './DetailView';
import {Theme} from './Theme';

export default class Main extends React.Component <undefined, undefined> {
    render() {
        return (
            <Theme>
                <Router basename="/nightmode">
                    <div>
                        <AdminDrawer/>

                        <Route exact path="/" />
                        <Route exact path="/guests" component={ListView} />
                        <Route exact path="/guests/:id" component={DetailView} />
                    </div>
                </Router>
            </Theme>
        )
    }
}
