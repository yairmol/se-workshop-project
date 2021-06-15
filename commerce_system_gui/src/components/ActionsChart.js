import React from 'react'
import {BarChart, Bar, Tooltip, XAxis, YAxis, ResponsiveContainer, Cell} from 'recharts';

const colors = ["#ed553b", "#f6d55c", "#3caea3", "#20639b",
    "#7268a6", "#32a852"];

class Chart extends React.Component {
    render() {
        return (
          <div>
            <ResponsiveContainer height={300} width="95%">
            <BarChart

                data={this.props.actions}
                margin={{
                    top: 5, right: 30, left: 20, bottom: 5,
                }}
            >
                <XAxis dataKey="action"/>
                <YAxis/>
                <Tooltip/>
                <Bar dataKey="num" fill="#82ca9d">
                    {this.props.actions.map((entry, index) => {
                      return <Cell fill={colors[index % colors.length]}/>
                    })}
                </Bar>
            </BarChart>
            </ResponsiveContainer>
              {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}
          </div>
        );
    }
}

export default Chart;