import * as React from 'react';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';

export class EventCard extends React.Component<undefined, undefined> {
    render() {
        return (
            <Card>
                <CardHeader
                    title="Headliner!"
                    subtitle="Blah blah blah"
                />

                <CardText>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Donec mattis pretium massa. Aliquam erat volutpat. Nulla facilisi.
                    Donec vulputate interdum sollicitudin. Nunc lacinia auctor quam sed pellentesque.
                    Aliquam dui mauris, mattis quis lacus id, pellentesque lobortis odio.
                </CardText>
            </Card>
        )
    }
}
