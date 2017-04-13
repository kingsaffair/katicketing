import * as React from 'react';

import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn
} from 'material-ui/Table';

import { FAIcon } from './FAIcon';

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
}

export interface IGuestListProps {
    guests: IGuest[]
}

export class GuestList extends React.Component < IGuestListProps, undefined > {
    constructor(props, context) {
        super(props, context);
    }

    render() {
        const tableItems = this.props.guests.map((guest, index) => {
            return (
                <TableRow key={guest.id}>
                    <TableRowColumn>{guest.fname} {guest.lname}</TableRowColumn>
                    <TableRowColumn>{guest.category}</TableRowColumn>
                </TableRow>
            );
        });

        return (
            <div>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHeaderColumn>Name</TableHeaderColumn>
                            <TableHeaderColumn>Category</TableHeaderColumn>
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
