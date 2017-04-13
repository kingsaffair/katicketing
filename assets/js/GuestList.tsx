import * as React from 'react';

import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn
} from 'material-ui/Table';

import FontIcon from 'material-ui/FontIcon';
import {green500} from 'material-ui/styles/colors'

// this needs to be updated relative to the Django stuff at some point
export enum Category {
    General,
    Worker,
    Musician,
    Committee,
    Shadow
}

export interface IGuest {
    fname: String
    lname: String
    category: String
    id: Number
    reentry_allowed: Boolean
}

type GuestSelectedCallback = (guests: IGuest[]) => void;

export interface IGuestListProps {
    guests: IGuest[]
    guestSelected: GuestSelectedCallback
}

export class GuestList extends React.Component < IGuestListProps, undefined > {
    constructor(props, context) {
        super(props, context);
    }

    selected = (row : string | number[]) => {
        if (row == 'all' || row.length != 1) {
            this.props.guestSelected(null);
        } else {
            this.props.guestSelected(this.props.guests[row[0]].id);
        }
    }

    render() {
        const tableItems = this.props.guests.map((guest, index) => {
            return (
                <TableRow key={guest.id}>
                    <TableRowColumn>{guest.fname} {guest.lname}</TableRowColumn>
                    <TableRowColumn>{guest.category}</TableRowColumn>
                    <TableRowColumn>{guest.reentry_allowed ? <FontIcon className="material-icons" color={green500}>check_circle</FontIcon> : null}</TableRowColumn>
                </TableRow>
            );
        });

        return (
            <div>
                <Table onRowSelection={this.selected}>
                    <TableHeader>
                        <TableRow>
                            <TableHeaderColumn>Name</TableHeaderColumn>
                            <TableHeaderColumn>Category</TableHeaderColumn>
                            <TableHeaderColumn>Reentry?</TableHeaderColumn>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {tableItems}
                    </TableBody>
                </Table>
            </div>
        )
    }
}
