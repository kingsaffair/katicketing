import React, {Component} from 'react';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';

import {white, deepPurple900} from 'material-ui/styles/colors';

console.log(darkBaseTheme)

darkBaseTheme.appBar = {
    textColor: white,
    color: deepPurple900
};

export class Theme extends Component {
    render() {
        return (<MuiThemeProvider muiTheme={getMuiTheme(darkBaseTheme)}>
            {this.props.children}
        </MuiThemeProvider>)
    }
}
