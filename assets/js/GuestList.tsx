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
import {green500, red500, blue500} from 'material-ui/styles/colors'

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
    payment_method: String
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

    reentry_icon = (guest) => {
        return guest.reentry_allowed ?
            <FontIcon className="fa fa-check-circle" color={green500}></FontIcon>
          : <FontIcon className="fa fa-times-circle" color={red500}></FontIcon>;
    }

    payment_icon = (guest) => {
        switch (guest.payment_method) {
            case 'ST':
                return <FontIcon className="fa fa-cc-stripe" color={blue500}></FontIcon>;
            case 'BT':
                return "Bank Transfer";
            case 'CB':
                return 'College Bill';
            case 'NO':
                return 'None';
            default:
                return null;
        }
    }

    render() {
        const tableItems = this.props.guests.map((guest, index) => {
            return (
                <TableRow key={guest.id}>
                    <TableRowColumn>{guest.fname} {guest.lname}</TableRowColumn>
                    <TableRowColumn>{guest.category}</TableRowColumn>
                    <TableRowColumn>{this.reentry_icon(guest)}</TableRowColumn>
                    <TableRowColumn>{this.payment_icon(guest)}</TableRowColumn>
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
                            <TableHeaderColumn>Re-entry?</TableHeaderColumn>
                            <TableHeaderColumn>Payment Method</TableHeaderColumn>
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
