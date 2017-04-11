import React, {Component} from 'react';

// Material UI
import AppBar from 'material-ui/AppBar';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';

const styles = {
    container: {
        margin: 0,
        padding: 0
    },
};

export class Main extends Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            open: false,
        };
    }

    render() {
        const standardActions = (
            <FlatButton
                label="Ok"
                primary={true}
            />
        );
        return (
            <div style={styles.container}>
                <AppBar title="King's Affair" />

            </div>
        )
    }
};