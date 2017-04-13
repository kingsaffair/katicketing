import * as React from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
// import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';

import {white, grey900} from 'material-ui/styles/colors';

lightBaseTheme.fontFamily = 'Open Sans, sans-serif';

// darkBaseTheme.appBar = {
//     textColor: white,
//     titleFontWeight: 100,
//     color: grey900
// };

export class Theme extends React.Component < undefined, undefined > {
    render() {
        return (
            <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
                {this.props.children}
            </MuiThemeProvider>
        )
    }
}
