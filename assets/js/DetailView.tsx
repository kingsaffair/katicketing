import * as React from 'react';

interface IDetailViewProps { match: any }

export class DetailView extends React.Component <IDetailViewProps, undefined> {
    constructor(props, context) {
        super(props, context);
    }

    render() {
        console.log(this.props);
        return (
            <div>
                { this.props.match.params.id }
            </div>
        )
    }
};
