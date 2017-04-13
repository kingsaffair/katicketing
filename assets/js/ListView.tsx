import * as React from 'react';

import axios from 'axios';

// Material UI
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';

import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar';

import {GuestList, IGuest} from './GuestList';

export interface MainState {
    open : boolean,
    guests : IGuest[],
    selectedId?: Number,
    query : any
};

export class ListView extends React.Component <undefined, MainState> {
    constructor(props, context) {
        super(props, context);

        this.state = {
            selectedId: null,
            query: null,
            open: false,
            guests: []
        };
    }

    componentDidMount = () => {
        this.sync("");
    }

    sync = (text) => {
        // if (this.state.query) {
        //     this.state.query.cancel();
        // }

        let query = axios.get(`/api/guests?search=${text}`);
        query.then(response => {
            this.setState({guests: response.data.results});
        });

        this.setState({query: query});
    }

    selected = (id) => {
        this.setState({selectedId: id});
    }

    showDetail = () => {
        console.log(this.state.selectedId);
    }

    render() {
        return (
            <div>
                <Toolbar>
                    <ToolbarGroup>
                        <TextField hintText="Search" onChange={(evt, val) => this.sync(val)}/>
                    </ToolbarGroup>
                    <ToolbarGroup>
                        <RaisedButton
                            label="View Details"
                            primary={true}
                            disabled={!this.state.selectedId}
                            onTouchTap={this.showDetail} />
                    </ToolbarGroup>
                </Toolbar>
                <GuestList guests={this.state.guests} guestSelected={this.selected}/>
            </div>
        )
    }
};