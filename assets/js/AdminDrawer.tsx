import * as React from 'react';

import {Link} from 'react-router-dom';

// Material UI
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import MenuItem from 'material-ui/MenuItem';

export interface AdminDrawerState { open: boolean };

export class AdminDrawer extends React.Component<undefined, AdminDrawerState> {
    constructor(props) {
        super(props);
        
        this.state = {
            open: false
        };        
    }

    toggle = () => {
        this.setState({
            open: !this.state.open
        });
    }

    render() {
        return (
            <div>
                <AppBar title="King's Affair" onLeftIconButtonTouchTap={this.toggle} />
                <Drawer open={this.state.open}>
                    <AppBar title="King's Affair" onLeftIconButtonTouchTap={this.toggle} />
                    <MenuItem><Link to="/guests">Lookup</Link></MenuItem>
                    <MenuItem>Announce</MenuItem>
                    <MenuItem>Team</MenuItem>
                </Drawer>
            </div>
        )
    }
}
