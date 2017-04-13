import * as React from 'react';

import axios from 'axios';

// Material UI
import AppBar from 'material-ui/AppBar';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import MenuItem from 'material-ui/MenuItem';
import TextField from 'material-ui/TextField';

import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';

import {EventCard} from './EventCard';
import {AdminDrawer} from './AdminDrawer';
import {GuestList, IGuest} from './GuestList';

const styles = {
    container: {
        padding: 10,
    },
};

export interface MainState { open: boolean, guests: IGuest[], query: any };

export class Main extends React.Component<undefined, MainState> {
    constructor(props, context) {
        super(props, context);

        this.state = {
            query: null,
            open: false,
            guests: []
        };
    }

    componentDidMount = () => {
        this.sync("");
    }

    sync = (text) => {
        if (this.state.query) {
            this.state.query.cancel();
        }

        let query = axios.get(`/api/guests?search=${text}`);
        query.then(response => {
            this.setState({
                guests: response.data.results
            });
        });

        this.setState({
            query: query
        });
    }

    render() {
        return (
            <div>
                <AdminDrawer />
                <div>
                    <Toolbar>
                        <ToolbarGroup>
                            <TextField hintText="Search" onChange={(evt, val) => this.sync(val)} />
                        </ToolbarGroup>
                    </Toolbar>
                    <GuestList guests={this.state.guests} />
                </div>
            </div>
        )
    }
};